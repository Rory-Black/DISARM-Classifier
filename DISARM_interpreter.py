import json
import time
import requests

OPENWEBUI_URL = "https://ai.datagaucho.com"
API_KEY = "sk-b3ce02f3eb5948f4b36a86c4ce23818e"
LARGE_MODEL = "qwen3-coder:30b"
FAST_MODEL = "qwen3-coder:30b"

TEST_DATA = """
Iran has taken a page from the Russian playbook: Passing off military groups as civilians for the sake of PR and plausible deniability.

Iranian state-backed advanced persistent threat (APT) groups have been masquerading as hacktivists, claiming attacks against Israeli critical infrastructure and air defense systems.

While threat actors in Gaza itself [have been radio silent](https://web.archive.org/web/20240221113558/https://www.darkreading.com/threat-intelligence/hamas-cyberattacks-ceased-after-october-7-attack-but-why), the majority of cyberattacks against Israel in recent months have been carried out by hacktivist operations and nation-state actors "playing them on TV," according to a new report from CrowdStrike.

These so-called "faketivists" have had a mixed impact on the Israeli-Gaza war thus far, claiming many public relations wins but leaving evidence of few truly disruptive attacks.

What's clearer are the benefits of the model itself: creating a layer of plausible deniability for the state, and the impression among the public that their attacks are grassroots-inspired. While this deniability has always been a key driver with state-sponsored cyberattacks, researchers characterized this instance as noteworthy for the effort behind the charade.

"We've seen a lot of hacktivist activity that seems to be nation-states trying to have that 'deniable' capability," Adam Meyers, CrowdStrike senior vice president for counter adversary operations said in a press conference this week. "And so these groups continue to maintain activity, moving from what was traditionally website defacements and DDoS attacks, into a lot of hack and leak operations."

## **Iran's Faketivists**

Faketivists can be nation-state actors — such as "Karma Power," the front for the Ministry of Intelligence-linked BANISHED KITTEN, or ["The Malek Team," in actuality SPECTRAL KITTEN](https://web.archive.org/web/20240221113558/https://www.darkreading.com/cyberattacks-data-breaches/israeli-defence-force-medical-data-hacked) — or corporate ones like HAYWIRE KITTEN — associated with Islamic Revolutionary Guard Corps contractor Emennet Pasargad, which at various times has operated under the nom de guerre Yare Gomnam Cyber Team and [al Toufan Team (aka Cyber Toufan)](https://web.archive.org/web/20240221113558/https://www.darkreading.com/cyberattacks-data-breaches/-cyber-toufan-hacktivists-leaked-100-plus-israeli-orgs-in-one-month).

To sell the persona, faketivists like to adopt the aesthetic, rhetoric, tactics, techniques, and procedures (TTPs), and sometimes the actual names and iconography associated with legitimate hacktivist outfits. Keen eyes will spot that they typically arise just after major geopolitical events, without an established history of activity, in alignment with the interests of their government sponsors.

Oftentimes, it's difficult to separate the faketivists from the hacktivists, as each might promote and support the activities of the other.

Post-Oct. 7 activity from Iran's faketivists — real and otherwise — has involved purported attacks against critical infrastructure and Israel's "Iron Dome" missile defense system, as well as frequent information operations.

And the former is often just a thin guise for the latter. While faketivists have achieved a select number of [breaches of note](https://web.archive.org/web/20240221113558/https://www.darkreading.com/ics-ot-security/pro-iran-attackers-access-multiple-water-facility-controllers), the majority of them appear to be opportunistic attacks of low material impact, intended to [boost the morale of one side and degrade the other's](https://web.archive.org/web/20240221113558/https://www.darkreading.com/cyberattacks-data-breaches/hackers-blast-violent-gaza-message-popular-israeli-movie-theater).

"We've seen disruptions targeting Israel, a lot of focus on things like air alert systems that alert about incoming missile strikes. We've seen attempts to disrupt infrastructure within Israel, for sure," Meyers said, adding that such activity is likely to continue in order to terrorize Israelis. "It's basically the same playbook that Russia used in Ukraine, of how can we terrorize the population and delegitimize their government, and cause them to distrust things."

## **The Gap Left by Hamas Threat Actors**

At the same time Iranian faketivism has shot up in Israel, cyber activity associated with Hamas has taken a nosedive.

Since the Oct. 7 terrorist attack in Israel, threat analysts have consistently found zilch from Hamas-connected cyber threat actors like Extreme Jackal (aka BLACKSTEM, MOLERATS) and Renegade Jackal (aka DESERTVARNISH, UNC718, Desert Falcons, Arid Viper).

This, CrowdStrike speculates in its report, might be explained by significant Internet disruptions in the region. Since the onset of war, it explained, connectivity in Gaza has been hampered by some combination of kinetic war, power outages, and distributed denial-of-service (DDoS) attacks.

Case-in-point: there is one Hamas-linked group — CruelAlchemy — whose command-and-control (C2) infrastructure has remained active since the onset of war. Though Gaza-connected, the group appears to be physically located in Turkey.

So while Hamas remains MIA online, its allies are making up the difference ([in volume, if not quality](https://web.archive.org/web/20240221113558/https://www.darkreading.com/cyberattacks-data-breaches/worldwide-hacktivists-take-sides-over-gaza-with-little-show)).

"The point is that APTs continue to proliferate. We see more and more threat actors every year, and more and more activity from those threat actors every single year," Meyers says.
"""
TEST_DATA_2 = """
After sending the Milan-Cortina crowd into a frenzy with his back flip in the figure skating team event, all eyes will be on US skater Ilia Malinin as he strives for individual Winter Olympic gold.

He made mistakes in the team event but was still the only participant to record more than 200 points, securing USA team gold by a single point ahead of Japan on Sunday.

That sums up the 21-year-old, the biggest star of his sport, who is set for global fame at Milan-Cortina 2026.

"It's his Olympics to lose," Olympic figure skating gold medallist Robin Cousins told BBC Sport. "After watching him over the last five years - he has grown. The talent was always there; he is otherworldly in that respect.

"Is it messy? Yes, but I watched him live and I got it. Now he has grown into that slightly quirky style - it isn't polished, and I don't want it to be.

"Anyone lucky enough to be in Milan, it will be one of those 'I was there' moments."

Malinin has not been beaten in competition for almost two and a half years. Competing in his first Olympics, he arrives with the nickname 'Quad God' having become the only skater to successfully land the quadruple axel.

The move requires a skater to launch themselves into a jump, spin four and a half times in the air, and cleanly land backwards.

Malinin did not pull out this move in the team event, although it was registered in his planned program. He landed triple axels instead - costing him points but still executed so perfectly that it provided a net benefit.

He made up for it by landing the first legal backflip at an Olympic Games since US champion Terry Kubicka in 1976 - after which it was banned for safety reasons.

Thanks in part to skaters like France's Surya Bonaly - who performed the move illegally but successfully at Nagano 1998 - the backflip is now legal again; and Malinin became the first to land it at the Games on only one foot.

So Malinin is already making history and winning golds, and he isn't even at his best yet.

He was due to only perform in the short program in the team event, but with USA's Olympic title from Beijing 2022 under threat by Japan, he agreed to perform in the free skate too.

"It was just such an honour, all my team-mates we have this passion for figure skating," he told the BBC after winning team gold. "And for many of us, this was just the start.

"I didn't want to go full capacity. I want to pace myself correctly going up to the individuals."

It is in the free skate where Malinin dominates. Japan's Yuma Kagiyama outshone Malinin in the team short program, just as he did in December's Grand Prix Final.

At the Grand Prix Final, Malinin was third after the short but still finished 30 points clear of the field after the free skate.

He has such an advantage because of a deadly combination of fearlessness and ability. His program for the free skate has a much higher technical score than any of his rivals - judges will give extra credit for ambition and he will also be rewarded with a higher component score.
"""
TA_FORMAT = """
{
“Tactics”: [“List of tactic names”]
}
"""
TA_SYSTEM_PROMPT = """
The AI assistant has been designed to understand and categorize user input by the given Tactics. 
When processing user input, the assistant must predict the Tactics from one of the pre-defined options specified. 
It is essential to note that an article may have multiple Tactics associated. If the user input is not relevant to any Tactics, 
the assistant should print nothing, indicating that the input does not align with the available categories. 
The user input will be in the following format:
{
Tactics: [{'name': "tactic name", 'description': "tactic description"}],
Article: "article text"
}
The agent MUST respond with the following JSON format: 
{
“Tactics”: [“List of tactic names”]
}

Respond only with valid JSON.
Do not add commentary.
"""
T_FORMAT = """
{
“Techniques”: [“List of external_id”]
}
"""
T_SYSTEM_PROMPT = """
The AI assistant has been designed to understand and categorize user input by the given techniques. When processing user input, the assistant must predict the techniques from one of the pre-defined options specified. It is essential to note that an article may have multiple Techniques associated. If the user input is not relevant to any techniques, the assistant should print nothing, indicating that the input does not align with the available categories. 
The user input will be in the following format:
{
Techniques: [{'external_id': "external_id"}, 'name': "technique name", 'description': "technique description"],
Article: "article text"
}
The agent MUST respond with the following JSON format: 
{
“Techniques”: [“List of external_id”]
}

Respond only with valid JSON.
Do not add commentary.
"""
JSON_FIX_SYSTEM_PROMPT = """
The agent has been designed to enforce and fix json formatting.
Respond only with valid JSON.
Do not add commentary or any other text.
"""
MAX_FIX_ATTEMPTS = 2
ANALYSIS_SYSTEM_PROMPT = """
The Agent is designed to provide an analysis of the execution log of a DISARM batch classification of an article.
The agent should focus on the tactics and techniques identified by the model at each round, and must report any inconsistencies where they did not persist due to parsing errors etc...
The agent should also focus on errors that occured during the execution of each round, such as parsing or incorrect classifications, and how effectively the model corrected these errors.
The user will input the execution log.
The agent MUST respond with a text analysis of the execution, focusing on the identified tactics and techniques, any inconsistencies in the results, and the errors that occurred during execution along with how effectively the model corrected them.
Respond only with the analysis.
"""

class DISARMClassifier:
    def __init__(self,
                 article_content=TEST_DATA,
                 large_model=LARGE_MODEL,
                 fast_model=FAST_MODEL,
                 max_fix_attempts=MAX_FIX_ATTEMPTS):
        self.LARGE_MODEL = large_model
        self.FAST_MODEL = fast_model
        self.max_fix_attempts = max_fix_attempts

        self.article_content = article_content
        self.total_failures = 0
        self.log_filename = None
        self.new_log_file()
        with open("DISARM.json", "r", encoding="utf-8") as f:
            self.disarm_json = json.load(f)

    def ask_openwebui(self, prompt, system_prompt=None, temperature=0.0, model=LARGE_MODEL, log=True):
        messages = []
        start_time = time.time()
        print(f"{model} thinking...")

        if system_prompt:
            messages.append({
                "role": "system",
                "content": system_prompt
            })

        messages.append({
            "role": "user",
            "content": prompt
        })

        response = requests.post(
            f"{OPENWEBUI_URL}/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": model,
                "messages": messages,
                "temperature": temperature,
                "stream": True,
                "seed": 48,
                "top_p": 1.0,
                "top_k": 1.0,
                "repeat_penalty": 1.0,
                "mirostat": 0,
            },
            stream=True,
            timeout=1000
        )

        full_response = ""

        for line in response.iter_lines():
            if not line:
                continue

            decoded = line.decode("utf-8")

            if not decoded.startswith("data: "):
                continue

            chunk = decoded.replace("data: ", "")

            if chunk == "[DONE]":
                break

            try:
                chunk_json = json.loads(chunk)
            except json.JSONDecodeError:
                continue

            if "choices" not in chunk_json:
                continue

            choice = chunk_json["choices"][0]
            delta = choice.get("delta", {})

            if "content" in delta:
                token = delta["content"]
                print(token, end="", flush=True)
                full_response += token

        print()  # newline after streaming
        print("\nDone in", round(time.time() - start_time, 2), "seconds")

        if log: self.log_result(full_response, prompt, round(time.time() - start_time, 2))
        return full_response

    # TODO add some manual checks to parse responses into json without relying on the model
    def prompt_valid_DISARM_response(self, prompt, system_prompt, available_classes, response_format):
        f_prev = self.total_failures
        start_time = time.time()
        classification_fix_system_prompt = f"""The agent has been designed to fix invalid json formatting into valid ones.
The agent must ensure that the fixed json formatting adheres to the available classifications provided by the user and does not include any classifications that were not identified in the previous response.
The agent MUST respond with the following JSON format: 
{response_format}

RESPOND ONLY WITH VALID JSON.
Do not add commentary or any other text.
It is essential not to add any classes that were not identified in the previous response. You are only fixing the formatting of the previously identified classes to match the valid json format and available classes provided by the user.
"""

        result_raw = self.ask_openwebui(prompt=prompt, system_prompt=system_prompt)
        result_parsed = self.responce_to_json(result_raw)
        # attempt to fix invalid classifications until valid ones are returned or a certain number of attempts is reached to avoid infinite loops
        attempts = 0
        while not self.valid_classifications(result_parsed, available_classes) and attempts < MAX_FIX_ATTEMPTS:
            error_code = f"ERROR: Model failed to return valid DISARM Classification: {result_raw}\n The agent MUST respond a JSON format from the list of available classifications: {available_classes}"
            print(error_code)
            fix_prompt = f"Invalid json format:\n{result_raw}\n\n Available classes: \n{available_classes}"
            result_raw = self.ask_openwebui(prompt= fix_prompt, system_prompt=classification_fix_system_prompt, model=self.FAST_MODEL)
            result_parsed = self.responce_to_json(result_raw)
            attempts += 1
            self.total_failures += 1
        # if not valid classification, recurse and try again
        if not self.valid_classifications(result_parsed, available_classes):
            print(f"ERROR: Model failed to return valid DISARM Classification after {MAX_FIX_ATTEMPTS} attempts: {result_raw}\n Recursing and trying again...")
            self.total_failures += 1
            result_parsed = self.prompt_valid_DISARM_response(prompt=prompt, system_prompt=system_prompt, available_classes=available_classes, response_format=response_format)
        self.log_round(available_classes, result_parsed, round(time.time() - start_time, 2), self.total_failures - f_prev)
        return result_parsed

    # TODO correct for infinite loops
    def responce_to_json(self, result_raw):
        parse_success = False
        while not parse_success:
            try:
                result_parsed = json.loads(result_raw)       
                parse_success = True         
            except json.JSONDecodeError:
                self.total_failures+=1
                error_code = f"ERROR: Failed to parse JSON from model response: {result_raw}\nModel failed to return valid JSON"
                print(error_code)
                fix_prompt = error_code + "\n Respond ONLY with valid JSON."
                result_raw = self.ask_openwebui(prompt=fix_prompt, system_prompt=JSON_FIX_SYSTEM_PROMPT, model=self.FAST_MODEL)
                try:
                    result_parsed = json.loads(result_raw)
                    parse_success = True
                except json.JSONDecodeError:
                    self.total_failures+=1
                    print(f"ERROR: Failed to parse JSON from model response: {result_raw}\nModel still failed to return valid JSON, trying again...")
        return result_parsed

    def parse_json_to_disarm(self, json, available_classes):
        # get class name aliases from disarm
        class_aliases = {}
        for obj in self.disarm_json["objects"]:
            if obj.get("type") == "x-mitre-tactic":
                if obj.get("x_mitre_shortname") in available_classes:
                    class_aliases[obj.get("name")] = obj.get("x_mitre_shortname")
            elif obj.get("type") == "attack-pattern":
                external_id = get_mitre_external_id(obj)
                if external_id:
                    class_aliases[obj.get("name")] = external_id
            
    def valid_classifications(self, json_results, available_classes):

        if not isinstance(json_results, dict):
            return False

        # Must contain exactly one of these keys
        valid_keys = ["Tactics", "Techniques"]
        present_keys = [k for k in valid_keys if k in json_results]

        if len(present_keys) != 1:
            return False

        key = present_keys[0]
        values = json_results[key]

        if not isinstance(values, list):
            return False

        # All returned items must be valid
        if not all(v in available_classes for v in values):
            return False

        return True

    def log_result(self, result, prompt, time):
        with open(self.log_filename, "a", encoding="utf-8") as f:
            f.write(f"Prompt:\n{prompt}\n\nResult:\n{result}\n\nTime: {time} seconds\n\n{'-'*50}\n\n")

    def log_round(self, available_classes, result, time, attempts):
        with open(self.log_filename, "a", encoding="utf-8") as f:
            f.write(f"ROUND SUMMARY:\nAvailable Classes:\n{available_classes}\n\nResult:\n{result}\n\nTime: {time} seconds\nFailures: {attempts}\n\n{'-'*50}\n\n")

    def log_final_result(self, total_tactics, total_techniques, time, failures):
        with open(self.log_filename, "a", encoding="utf-8") as f:
            f.write(f"EXECUTION SUMMARY:\nTotal Identified Tactics: {total_tactics}\nTotal Identified Techniques: {total_techniques}\n\nTotal execution time: {time} seconds\n\nFailures:\n{failures}")
        self.log_analysis()

    def log_analysis(self):
        # retrieve the execution log
        with open(self.log_filename, "r", encoding="utf-8") as f:
            execution_log = f.read()
            prompt = f"Provide a detailed anaysis of this execution log: \n\n {execution_log}"
            analysis = self.ask_openwebui(prompt=prompt, system_prompt=ANALYSIS_SYSTEM_PROMPT, model=self.LARGE_MODEL, log=False)
        with open(self.log_filename, "a", encoding="utf-8") as f:
            f.write(f"\n\nEXECUTION ANALYSIS:\n{analysis}")

    def new_log_file(self):
        timestamp = time.strftime("%Y%m%d-%H%M%S")
        self.log_filename = f"exe_logs/DISARM_log_{timestamp}.txt"
        with open(self.log_filename, "w", encoding="utf-8") as f:
            f.write(f"DISARM Log File - Created on {timestamp}\nSETUP:\nLarge Model: {self.LARGE_MODEL}\nFast Model: {self.FAST_MODEL}\nTemperature: 0.0\nMax Fix Attempts: {MAX_FIX_ATTEMPTS}\n\n{'='*50}\n\n")
            
    def identify_tactics(self, article_content):
        tactics = []
        for obj in self.disarm_json["objects"]:
            if obj.get("type") == "x-mitre-tactic":
                tactics.append(obj)

        filtered_tactics = []
        available_classifications = []

        # filter the tactic json data by name and description
        for tactic in tactics:
            # print(tactic["name"])
            filtered_tactics.append({
                "name": tactic.get("x_mitre_shortname"),
                "description": tactic.get("description")
            })
            available_classifications.append(tactic.get("x_mitre_shortname"))

        # print(filtered_tactics)

        ta_prompt = f"""
{{
"Tactics": {json.dumps(filtered_tactics, indent=2)},
"Article": {json.dumps(article_content)}
}}
"""

        # print(ta_prompt)
        
        print("Identifying Tactics...")
        ta_result_parsed = self.prompt_valid_DISARM_response(prompt=ta_prompt, system_prompt=TA_SYSTEM_PROMPT, available_classes=available_classifications, response_format=TA_FORMAT)
        ta_result_list = ta_result_parsed.get("Tactics", [])    
        print("Identified Tactics: " + str(ta_result_list))
        return ta_result_list

    def identify_techniques_for_tactic(self, tactic, article_content):
        print("Testing for tactic: " + tactic)
        techniques = []
        filtered_techniques = []
        available_classifications = []
        for obj in self.disarm_json["objects"]:
            if obj.get("type") == "attack-pattern":
                for phase in obj.get("kill_chain_phases", []):
                    if phase.get("phase_name") == tactic:
                        techniques.append(obj)
                        # print(obj["name"])

        for technique in techniques:
            filtered_techniques.append({
                "external_id": get_mitre_external_id(technique),
                "description": technique.get("description"),
            })
            available_classifications.append(get_mitre_external_id(technique))
        
        t_prompt = f"""
    {{
    "Techniques": {json.dumps(filtered_techniques, indent=2)},
    "Article": {json.dumps(article_content)}
    }}
"""
        
        # print(t_prompt)
        
        t_result = self.prompt_valid_DISARM_response(prompt=t_prompt, system_prompt=T_SYSTEM_PROMPT, available_classes=available_classifications, response_format=T_FORMAT)
        t_result_list = t_result.get("Techniques", [])
        print("Identified Techniques: " + str(t_result_list))
        return t_result_list

    # MAIN EXECUTION
    def batch_clf(self, article_content):
        self.total_failures = 0
        start_time = time.time()

        #TACTICS
        tactics = self.identify_tactics(article_content)

        #TECHNIQUES LOOP
        total_techniques = []
        for tactic in tactics:
            techniques = self.identify_techniques_for_tactic(tactic, article_content)
            total_techniques.extend(techniques)

        print("Total Identified Techniques: " + str(total_techniques))
        print("\nTotal execution time: " + str(round(time.time() - start_time, 2)) + " seconds")
        self.log_final_result(tactics,total_techniques, round(time.time() - start_time, 2), self.total_failures)

def get_mitre_external_id(obj):
    for ref in obj.get("external_references", []):
        if ref.get("source_name") == "mitre-attack":
            return ref.get("external_id")
    return None

def main():
    interpreter = DISARMClassifier()
    interpreter.batch_clf(article_content=TEST_DATA)

if __name__ == "__main__":
    main()