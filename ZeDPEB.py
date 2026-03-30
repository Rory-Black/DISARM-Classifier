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
from enum import Enum
import numpy as np
import re

from rouge_score import rouge_scorer
from DISARM_DATA_MASTER import DISARMDataMaster
from DISARM_interpreter import DISARMClassifier, get_mitre_external_id

class ClfMode(Enum):
    SELECT_ALL = "SelectAll"
    BATCH_FAST = "FastBatch"
    BATCH_FULL = "FullBatch"
    SINGLE = "Single"

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

def new_log_file(mode, model, enbl_precision, num_tests):
    global log_filename
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    log_filename = f".ZeDPEB_logs/log_{timestamp}_{mode.value}_{num_tests}.txt"
    log_to_file(f"ZeDPEB Log File - Created on {timestamp}\n\n{'='*50}")
    setup_str = f"""
SETUP
mode  - {mode}
model - {model}
test  - Recall {"& Precision" if enbl_precision else "only (Expect Deviations Technique recall for FastBatchClf)"}
{'='*50}
"""
    log_to_file(setup_str)

# gets the part of the technique string that prepends the '.' 
def technique_partial(technique):
    return technique.split('.')[0]

def partial_match(correct_technique, identified_techniques):
    for identified_technique in identified_techniques:
        if technique_partial(correct_technique) == technique_partial(identified_technique):
            return True
    return False

def calc_precision(n_pos, n_false):
    try:
        p = n_pos / (n_pos + n_false)
    except ZeroDivisionError:
        return 0
    return p

def calc_f1(precision, recall):
    return (2 * precision * recall) / (precision + recall)

def test_rationale(technique_positives, incident_id, article_content, disarm_classifer, mode):
    print_log(f"\nRationale Test for incident {incident_id}\n")
    # get rationales with faithfullness checks
    model_rationales, comprehensiveness, sufficiency = get_model_rationales(incident_id, article_content, technique_positives, disarm_classifer, mode)
    ave_recall, ave_precision, f1 = rationale_plausability(model_rationales, incident_id)
    log_rationale_stats(comprehensiveness, sufficiency, ave_recall, ave_precision, f1)
    return comprehensiveness, sufficiency, ave_recall, ave_precision, f1

# TODO add methods for each mode
def get_model_rationales(incident_id, article_content, external_ids, disarm_classifer, mode):
    # extracts the models rationales and checks how faithfull they are
    # depends on classificaton mode
    match mode:
        case ClfMode.SELECT_ALL:
            # rationales stored as JSON object list with external_ids linked to lists of quotes (rationales)
            rationales = disarm_classifer.identify_rationales(external_ids)
        case ClfMode.BATCH_FAST:
            pass
        case ClfMode.BATCH_FULL:
            rationales = disarm_classifer.identify_rationales(external_ids)
            pass
        case ClfMode.SINGLE:
            pass
    comprehensiveess = rationale_comprehensiveness(incident_id, article_content, rationales, disarm_classifer, mode)
    sufficiency = rationale_sufficiency(incident_id, article_content, rationales, disarm_classifer, mode)
    
    return rationales, comprehensiveess, sufficiency 

def log_rationale_stats(comp, suff, recall, prec, f1):
    log = f"""{'.'*50}
Rationale test results:
    Faithfullness:
        Comprehensiveness: {comp}
        Sufficiency:       {suff}
    Plausability (Rouge Scores):
        Recall:    {recall}
        Precision: {prec} 
        F1:        {f1}
{'.'*50}"""
    print_log(log)
    
# Faithfullness metrics
def rationale_comprehensiveness(incident_id, article_content, model_rationales, disarm_classifer, mode):
    # check if removing model rationale from the model input changes the classification 
    return 0

def rationale_sufficiency(incident_id, article_content, model_rationales, disarm_classifer, mode):
    # check if removing everything except the model rationale from the model input changes the classification
    return 0

# TODO
def rationale_plausability(model_rationales, incident_id):
    # actually scores how similar the models rationale is to the 'gold' rationale
    total_recall = []
    total_precision = []
    total_f1 = []
    print_log(f"\nRationale Plausability test for incident: {incident_id}")
    # returns a list of tuples (technique, quotes)
    gold_rationales = get_gold_rationales(incident_id=incident_id)
    for gold in gold_rationales:
        technique, gold_quotes = gold
        # get the model rationale for the associated gold technique rationale
        model = next((m for m in model_rationales if m[0] == technique), None)
        if model is None:
            # skip if not identified by model
            continue
        _, model_quotes = model
        recall, precision, f1 = rationale_rouge(model_quotes, gold_quotes)
        log = f"""
Rationale score for technique: {technique}
    Recall: {recall}
    Precision: {precision}
    F1: {f1}
"""
        print_log(log)
        total_recall.append(recall)
        total_precision.append(precision)
        total_f1.append(f1)

    #calculate average scores
    ave_recall = np.average(total_recall)
    ave_precision = np.average(total_precision)
    ave_f1 = np.average(total_f1)

    return ave_recall, ave_precision, ave_f1

def get_gold_rationales(incident_id):
    incident_data = DISARMDataMaster().get_incident_techniques_with_desc(incidentid=incident_id)
    rationales = []
    for d in incident_data:
        #split descriptions into quotes
        (external_id, desc) = d
        quotes = re.findall(r"<i>(.*?)</i>", desc, re.IGNORECASE)
        if quotes == []:
            quotes = re.findall(r"\_(.*?)\_", desc, re.IGNORECASE)
        rationales.append((external_id, quotes))
    return rationales

def normalise_rationale(quotes):
    full_rationale = ""
    for q in quotes:
        full_rationale += q
    return full_rationale

def rationale_rouge(model_quotes, gold_quotes):
    model_quotes = normalise_rationale(model_quotes)
    gold_quotes = normalise_rationale(gold_quotes)

    scorer = rouge_scorer.RougeScorer(['rouge1'], use_stemmer=True)
    scores = scorer.score(model_quotes, gold_quotes)

    return scores['rouge1']

# Todo: implement more statistics
def test_clf(model, mode=ClfMode.BATCH_FULL, num_tests=-1, checkpoint=0, enbl_precision=True, enbl_rationale=False):
    is_fast_batch = mode == ClfMode.BATCH_FAST 

    start_time = time.time()
    disarm_data = DISARMDataMaster()
    new_log_file(mode, model, enbl_precision, num_tests)

    incident_ids = disarm_data.get_incident_ids()
    # variables to keep track of overall performance
    ta_total = t_total = ta_mtchs_total = t_mtchs_total = t_abs_mtchs_total = t_prt_mtchs_total = 0
    ta_false_total = t_false_total = t_abs_false_total = 0
    #rationales
    r_comp = []
    r_suff = []
    r_rec = [] 
    r_prec = [] 
    r_f1 = []
    
    # incident loop
    for incident_id in incident_ids:
        # break loop if number of tests reached
        if num_tests == 0:
            break
        tactic_positives = 0
        technique_abs_positives = 0
        technique_abs_positives_list = []
        technique_partial_positives = 0

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
        if len(article_content) < 100:
            print_log(f"Skipping incident {incident_id} - insignificant amount of article content retrieved ({len(article_content)})\n")
            continue

        ta_total += len(article_tactics)
        t_total += len(article_techniques)
        
        disarm_classifer = DISARMClassifier(article_content=article_content, large_model=model)
        print_log(f"Testing for incident with ID: {incident_id} \n{f"Required Tactics: {article_tactics}\n" if is_fast_batch else ""}Required Techniques: {article_techniques}\n")
        print_log(f"Classifier log created in: {disarm_classifer.log_filename}\n")
        print_log(f"Article Character Length: {len(article_content)}\n")

        identified_techniques = []
        identified_tactics = []

        if mode == ClfMode.BATCH_FAST or mode == ClfMode.BATCH_FULL:
            if enbl_precision or mode == ClfMode.BATCH_FAST:
                identified_tactics, identified_techniques = disarm_classifer.batch_clf(mode == ClfMode.BATCH_FAST)
                for required_tactic in article_tactics:
                    if required_tactic in identified_tactics:
                        tactic_positives+=1
            else:
                for required_tactic in article_tactics:
                    # perform technique classifications (ONLY for relevant tactics, no need to do full batchClf):
                    identified_techniques += disarm_classifer.identify_techniques_for_tactic(required_tactic)
        elif mode == ClfMode.SELECT_ALL:
            identified_techniques = disarm_classifer.select_all_clf()
        elif mode == ClfMode.SINGLE:
            if enbl_precision:
                identified_techniques = disarm_classifer.single_clf()
            else:
                # only check relevant techniques, no need to do full clf
                for required_technique in article_techniques:
                    identified_techniques += disarm_classifer.identify_techniques(techniques=[required_technique])

        print(f"Techniques identified by model: {identified_techniques}")
        for required_technique in article_techniques:
            if required_technique in identified_techniques:
                technique_abs_positives+=1
                technique_abs_positives_list.append(required_technique)
            elif partial_match(required_technique, identified_techniques):
                technique_partial_positives+=1
        # record results
        technique_positives = technique_abs_positives + technique_partial_positives
        ta_false = len(identified_tactics) - tactic_positives
        t_false = len(identified_techniques) - (technique_positives)
        t_abs_false = len(identified_techniques) - (technique_abs_positives)
        # update totals
        ta_mtchs_total += tactic_positives
        t_mtchs_total += technique_positives
        t_abs_mtchs_total += technique_abs_positives
        t_prt_mtchs_total += technique_partial_positives

        ta_false_total += ta_false
        t_false_total += t_false
        t_abs_false_total += t_abs_false

        results_log = f"""Results:
{f"Identified tactics({len(identified_tactics)}): {identified_tactics}" if is_fast_batch else ""}
Identified techniques({(len(identified_techniques))}): {identified_techniques}

Recall:
{f"Correct Tactics: {tactic_positives}/{len(article_tactics)}" if is_fast_batch else ""}
Correct Techniques: {technique_positives}/{len(article_techniques)}
    Absolute technique matches: {technique_abs_positives}
    Partial technique matches: {technique_partial_positives}

Precision:
{f"Tactics: {calc_precision(tactic_positives, ta_false)}" if is_fast_batch else ""}
Techniques: {calc_precision(technique_positives, t_false)}
    Absolute Techniques: {calc_precision(technique_abs_positives, t_abs_false)}
"""
        print_log(results_log)
        
        if enbl_rationale and technique_abs_positives > 0:
            # test and log model rationale
            c, s, r, p, f = test_rationale(technique_abs_positives_list, incident_id, article_content, disarm_classifer, mode) 
            r_comp.append(c)
            r_suff.append(s)
            r_rec.append(r)
            r_prec.append(p)
            r_f1.append(f)
        elif technique_abs_positives <= 0:
            print_log(f"\nUnable to test for rationales - no absolute technique matches\n")
        
        print_log('-'*50)
        num_tests-=1
    final_log = f"""
{'='*50}
Final Results:
{'-'*50}
Recall:
{f"Correct Tactics: {ta_mtchs_total}/{ta_total} \t ({(ta_mtchs_total/ta_total)*100}%)" if is_fast_batch else ""}
Correct Techniques: {t_mtchs_total}/{t_total} \t ({((t_mtchs_total)/t_total)*100}%)
    Absolute technique matches: {t_abs_mtchs_total} \t ({(t_abs_mtchs_total/t_total)*100}%)
    Partial technique matches: {t_prt_mtchs_total} \t ({(t_prt_mtchs_total/t_total)*100}%)
{'-'*50}
Precision:
{f"Tactics: {calc_precision(ta_mtchs_total, ta_false_total)}" if is_fast_batch else ""}
Techniques: {calc_precision(t_mtchs_total, t_false_total)}
    Absolute Techniques: {calc_precision(t_abs_mtchs_total, t_abs_false_total)}
"""
    if enbl_rationale:
        final_log += f"""{'-'*50}
Rationale test results:
    Faithfullness:
        Comprehensiveness: {np.average(r_comp)}
        Sufficiency:       {np.average(r_suff)}
    Plausability (Rouge Scores):
        Recall:    {np.average(r_rec)}
        Precision: {np.average(r_prec)} 
        F1:        {np.average(r_f1)}
{'-'*50}"""
    final_log += f"""
Time Taken: {round((time.time() - start_time)/60, 2)} minuites
{'='*50}"""
    print_log(final_log)

def print_log(str):
    print(str)
    log_to_file(str)

def main():
    large_model = "Qwen/Qwen3.5-35B-A3B"
    test_clf(model=large_model, mode=ClfMode.BATCH_FULL,num_tests=5, checkpoint=0, enbl_precision=True, enbl_rationale=True)
    # print(DISARMDataMaster().get_incident_techniques_with_desc(incidentid='I00064'))
    # print(get_gold_rationales('I00064'))

if __name__ == "__main__":
    main()
