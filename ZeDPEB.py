# Benchmarking software for the DISARM Interpreter

# for every incident file:
    # get the required techniques and tactics for the benchmark
    # Identify tactics with model
    # check if tactics identified contain required ones
    # For ONLY the tactics relevant to that benchmark, get the techniques
    # Check the identified techniques contain the required ones

import time
import json
import requests
from bs4 import BeautifulSoup

from DISARM_DATA_MASTER import DISARMDataMaster
from DISARM_interpreter import DISARMClassifier, get_mitre_external_id

def get_related_tactic(technique_external_id):
        with open("DISARM.json", "r", encoding="utf-8") as f:
            disarm_json = json.load(f)
            for obj in disarm_json["objects"]:
                if obj.get("type") == "attack-pattern":
                    if get_mitre_external_id(obj) == technique_external_id:
                        for phase in obj.get("kill_chain_phases", []):
                            return phase.get("phase_name")
            return None

# retrieve the incident data from the disarm xlsx file
def retrieve_incident_data(disarm_data, incident_id):
    #fetch incident data
    article_techniques = disarm_data.get_incident_techniques(incident_id)
    #break if no techniques
    if len(article_techniques) <= 0: return None
    article_tactics = []
    for tech in article_techniques:
        tac = get_related_tactic(tech)
        if tac not in article_tactics:
            article_tactics.append(tac)
    #fetch the incident url content
    urls = disarm_data.get_incident_urls(incident_id)
    if urls == []: 
        return None
    elif len(urls) > 1:
        print_log("Warning: Multiple urls for incident: ", incident_id)
    article_content = None
    print("Fetching Article Content")
    response = requests.get(url=urls[0], headers={"User-Agent": "Mozilla/5.0"})
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        paragraphs = soup.find_all("p")
        article_content = "\n".join(p.get_text() for p in paragraphs)
        # print(article_content)
        print(f"Done. Fetched article of length {len(article_content)}")
        print_log(f"{'-'*50}\nRetrieved article from {urls[0]}\n")
    else:
        print_log(f"\nError when attempting to fetch incident url content. Code: {response.status_code}\n")
    
    return article_content, article_tactics, article_techniques
    
def log_to_file(message):
    # retrieve the execution log
    with open(log_filename, "a", encoding="utf-8") as f:
        f.write(message)

def new_log_file():
    global log_filename
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    log_filename = f"ZeDPEB_logs/log_{timestamp}.txt"
    log_to_file(f"ZeDPEB Log File - Created on {timestamp}\n\n{'='*50}\n\n")

# gets the part of the technique string that prepends the '.' 
def technique_partial(technique):
    return technique.split('.')[0]

def partial_match(correct_technique, identified_techniques):
    for identified_technique in identified_techniques:
        if technique_partial(correct_technique) == technique_partial(identified_technique):
            return True
    return False

def test_batch_clf(num_tests=-1, checkpoint=0):
    start_time = time.time()
    disarm_data = DISARMDataMaster()
    new_log_file()
    incident_ids = disarm_data.get_incident_ids()
    # variables to keep track of overall performance
    ta_total = t_total = ta_mtchs_total = t_abs_mtchs_total = t_prt_mtchs_total = 0
    
    # incident loop
    for incident_id in incident_ids:
        # break loop if number of tests reached
        if num_tests == 0:
            break
        tactic_matches = 0
        technique_matches = 0
        technique_partial_matches = 0

        # get the incident data
        result = retrieve_incident_data(disarm_data, incident_id)

        # skip if no url/data is available
        if result is None:
            print_log(f"Skipping incident {incident_id} - missing data\n")
            continue
        if checkpoint > 0:
            print_log(f"Skipping incident {incident_id} by user request\n")
            checkpoint -= 1
            continue
        article_content, article_tactics, article_techniques = result
        ta_total += len(article_tactics)
        t_total += len(article_techniques)
        
        disarm_classifer = DISARMClassifier()
        print_log(f"Testing for incident with ID: {incident_id}\nTactics: {article_tactics}\nTechniques: {article_techniques}\n")
        print_log(f"Classifier log created in: {disarm_classifer.log_filename}\n")
        print_log(f"Article Character Length: {len(article_content)}\n")

        # Perform Tactic classifications:
        identified_tactics = disarm_classifer.identify_tactics(article_content)
        # reset chat history for techniques (to emulate normal execution of batchCLF loop)
        disarm_classifer.conversation_history_main = []
        identified_techniques = []
        print(f"Tactics identified by model: {identified_tactics}")
        for required_tactic in article_tactics:
            if required_tactic in identified_tactics:
                tactic_matches+=1
            # Perform nested technique classifications (ONLY for relevant tactics, no need to do full batchClf):
            identified_techniques += disarm_classifer.identify_techniques_for_tactic(required_tactic, article_content)
        print(f"Techniques identified by model: {identified_techniques}")
        for required_technique in article_techniques:
            if required_technique in identified_techniques:
                technique_matches+=1
            elif partial_match(required_technique, identified_techniques):
                technique_partial_matches+=1
        # record results
        ta_mtchs_total += tactic_matches
        t_abs_mtchs_total += technique_matches
        t_prt_mtchs_total += technique_partial_matches
        results_log = f"""Results:
Identified tactics({len(identified_tactics)}): {identified_tactics}
Identified techniques({(len(identified_techniques))}): {identified_techniques}

Correct Tactics: {tactic_matches}/{len(article_tactics)}
Correct Techniques: {technique_matches + technique_partial_matches}/{len(article_techniques)}
    Absolute technique matches: {technique_matches}
    Partial technique matches: {technique_partial_matches}
{'-'*50}"""
        print_log(results_log)
        num_tests-=1
    final_log = f"""
{'='*50}
Final Results:
{'-'*50}
Correct Tactics: {ta_mtchs_total}/{ta_total} \t ({(ta_mtchs_total/ta_total)*100}%)
Correct Techniques: {t_abs_mtchs_total + t_prt_mtchs_total}/{t_total} \t ({((t_abs_mtchs_total+t_prt_mtchs_total)/t_total)*100}%)
    Absolute technique matches: {t_abs_mtchs_total} \t ({(t_abs_mtchs_total/t_total)*100}%)
    Partial technique matches: {t_prt_mtchs_total} \t ({(t_prt_mtchs_total/t_total)*100}%)
Time Taken: {round((time.time() - start_time)/60, 2)} minuites
{'='*50}"""
    print_log(final_log)

def test_single_clf(num_tests=-1, checkpoint=0):
    start_time = time.time()
    disarm_data = DISARMDataMaster()
    new_log_file()
    incident_ids = disarm_data.get_incident_ids()
    # variables to keep track of overall performance
    t_total = ta_mtchs_total = t_abs_mtchs_total = t_prt_mtchs_total = 0
    
    # incident loop
    for incident_id in incident_ids:
        # break loop if number of tests reached
        if num_tests == 0:
            break
        technique_matches = 0
        technique_partial_matches = 0

        # get the incident data
        result = retrieve_incident_data(disarm_data, incident_id)

        # skip if no url/data is available
        if result is None:
            print_log(f"Skipping incident {incident_id} - missing data\n")
            continue
        if checkpoint > 0:
            print_log(f"Skipping incident {incident_id} by user request\n")
            checkpoint -= 1
            continue
        article_content, article_tactics, article_techniques = result
        t_total += len(article_techniques)
        
        disarm_classifer = DISARMClassifier()
        print_log(f"Testing for incident with ID: {incident_id}\nTechniques: {article_techniques}\n")
        print_log(f"Classifier log created in: {disarm_classifer.log_filename}\n")
        print_log(f"Article Character Length: {len(article_content)}\n")

        # perform technique classification for all techniques
        identified_techniques = disarm_classifer.identify_techniques(article_content)
        print(f"Techniques identified by model: {identified_techniques}")
        for required_technique in article_techniques:
            if required_technique in identified_techniques:
                technique_matches+=1
            elif partial_match(required_technique, identified_techniques):
                technique_partial_matches+=1
        # record results
        t_abs_mtchs_total += technique_matches
        t_prt_mtchs_total += technique_partial_matches
        results_log = f"""Results:
Identified techniques({(len(identified_techniques))}): {identified_techniques}

Correct Techniques: {technique_matches + technique_partial_matches}/{len(article_techniques)}
    Absolute technique matches: {technique_matches}
    Partial technique matches: {technique_partial_matches}
{'-'*50}"""
        print_log(results_log)
        num_tests-=1

    final_log = f"""
{'='*50}
Final Results:
{'-'*50}
Correct Techniques: {t_abs_mtchs_total + t_prt_mtchs_total}/{t_total} \t ({((t_abs_mtchs_total+t_prt_mtchs_total)/t_total)*100}%)
    Absolute technique matches: {t_abs_mtchs_total} \t ({(t_abs_mtchs_total/t_total)*100}%)
    Partial technique matches: {t_prt_mtchs_total} \t ({(t_prt_mtchs_total/t_total)*100}%)
Time Taken: {round((time.time() - start_time)/60, 2)} minuites
{'='*50}"""
    print_log(final_log)

def print_log(str):
    print(str)
    log_to_file(str)

def main():
    large_model = "gpt-oss:latest"
    fast_model = "gpt-oss:latest"
    test_single_clf(num_tests=5, checkpoint=0)

if __name__ == "__main__":
    main()
