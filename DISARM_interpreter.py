import json
import time
import requests
from openai import OpenAI

client = OpenAI(
    base_url="http://localhost:8000/v1",
    api_key="EMPTY"
)

OPENWEBUI_URL = "https://ai.datagaucho.com"
VLLM_URL = "http://localhost:8000"

API_KEY = "sk-b3ce02f3eb5948f4b36a86c4ce23818e"
LARGE_MODEL = "Qwen/Qwen3.5-35B-A3B"

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
TEST_DATA_3 = """
A United States Navy submarine sank an Iranian ship with a single torpedo as the frigate was transiting the Indian Ocean, marking the first such kill by a U.S. submarine since World War II, the Pentagon confirmed on Wednesday.

Defense Secretary Pete Hegseth confirmed the strike during a Pentagon press briefing on Operation Epic Fury alongside Chairman of the Joint Chiefs of Staff Gen. Dan Caine.

“Yesterday, in the Indian Ocean ... an American submarine sunk an Iranian warship that thought it was safe in international waters,” Hegseth said. “Instead, it was sunk by a torpedo. Quiet death. The first sinking of an enemy ship by a torpedo since World War II.”

The identity of the fast-attack boat was not revealed, as is custom for operational security surrounding submarine operations.

The strike occurred off the southern coast of Sri Lanka, according to Reuters, which would indicate the action occurred in the U.S. Indo-Pacific Command area of responsibility.

The IRIS Dena, a Moudge-class frigate assigned to the Southern Fleet of the Islamic Republic of Iran Navy, was in the region after reportedly taking part in a naval drill in the Bay of Bengal.

Sri Lankan Foreign minister Vijitha Herath said 180 people were on board the IRIS Dena. Thirty-two people were subsequently rescued by Sri Lankan naval personnel.

Commander Buddhika Sampath, a Sri Lankan navy spokesman, said the rescue effort was also recovering bodies from the scene.

“For the first time since 1945, a United States Navy fast attack submarine has sunk an enemy combatant ship using a single Mk-48 torpedo to achieve immediate effect, sending the warship to the bottom of the sea,” Caine said during the press briefing Wednesday.

“This is an incredible demonstration of America’s global reach. To hunt, find and kill an out-of-area deployer is something that only the United States can do at this type of scale.”

Caine added that, to date, the U.S. has hit over 2,000 total targets across Iran and destroyed more than 20 of the Islamic Republic’s naval vessels.

The campaign has “effectively neutralized, at this point in time, Iran’s major naval presence in theater,” he said.

Strikes on infrastructure and naval capability by the vast assembly of U.S. forces in the region are expected to continue over the next 24 to 48 hours, Caine noted.

“We’ll continue to assess our progress against the military objectives,” he said.
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
"""

T_SYSTEM_PROMPT = """
The AI assistant has been designed to understand and categorize user input by the given techniques. When processing user input, the assistant must predict the techniques from one of the pre-defined options specified. It is essential to note that an article may have multiple Techniques associated. If the user input is not relevant to any techniques, the assistant should print nothing, indicating that the input does not align with the available categories. 
The user input will be in the following format:
{
Article: "article text"
Techniques: [{'external_id': "external_id"}, 'name': "technique name", 'description': "technique description"],
}
The agent MUST respond with the following JSON format: 
{
“Techniques”: [“List of external_id”]
}
"""
ANALYSIS_SYSTEM_PROMPT = """
The Agent is designed to provide an analysis of the execution log of a DISARM batch classification of an article.
The agent should focus on the tactics and techniques identified by the model at each round, and must report any inconsistencies where they did not persist due to parsing errors etc...
The agent should also focus on errors that occured during the execution of each round, such as parsing or incorrect classifications, and how effectively the model corrected these errors.
The user will input the execution log.
The agent MUST respond with a text analysis of the execution, focusing on the identified tactics and techniques, any inconsistencies in the results, and the errors that occurred during execution along with how effectively the model corrected them.
Respond only with the analysis.
"""
T_RAT_SYSTEM_PROMPT = """
The AI assistant has been designed to understand and categorize user input by the given techniques. 
When processing user input, for each technique given by the user, the assistant must select quotes from the article that represent the rationale behind each technique classification. 
It is essential to note that an article may have multiple Techniques associated. 
The user input will be in the following format:
{
Article: "article text"
Techniques: [{'external_id': "external_id"}, 'name': "technique name", 'description': "technique description"],
}
The agent MUST respond with the following JSON format: 
{
  "results": [
    {
      "technique": "external_id",
      "quotes": [
        "quote 1",
        "quote 2"
      ]
    }
  ]
}
The agent MUST 
- return one object per technique
- include at least one quote per technique
- ensure quotes are direct substrings of the article
The agent should be greedy in it's quote selection: quote anything that would support the classification
"""
class DISARMClassifier:
    def __init__(self,
                 article_content=TEST_DATA,
                 large_model=LARGE_MODEL):
        self.LARGE_MODEL = large_model

        self.article_content = article_content
        self.log_filename = None
        self.conversation_history_main = []
        self.conversation_history_debug = []

        self.new_log_file()
        with open("DISARM.json", "r", encoding="utf-8") as f:
            self.disarm_json = json.load(f)

    def set_article_content(self, article_content):
        self.article_content=article_content

    def get_article_content(self):
        return self.article_content

    def prompt_llm_response(self, prompt, system_prompt=None, log=True, messages = None, response_format=None):
        if response_format == None:
            response_format = self.response_format
        start_time = time.time()
        print(f"{self.LARGE_MODEL} thinking...")

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ]

        self.log_debug(f"\nChat history input to model: {'\n'.join(str(m) for m in messages)}\n")
        self.log_to_file(f"\nPrompt: {prompt}\n")

        response = self.vllm_response(messages=messages, response_format=response_format)

        full_response = ""

        # use for streaming 
        # for line in response.iter_lines():
        #     if not line:
        #         continue

        #     decoded = line.decode("utf-8")

        #     if not decoded.startswith("data: "):
        #         continue

        #     chunk = decoded.replace("data: ", "")

        #     if chunk == "[DONE]":
        #         break

        #     try:
        #         chunk_json = json.loads(chunk)
        #     except json.JSONDecodeError:
        #         continue

        #     if "choices" not in chunk_json:
        #         continue

        #     choice = chunk_json["choices"][0]
        #     delta = choice.get("delta", {})

        #     if "content" in delta:
        #         token = delta["content"]
        #         print(token, end="", flush=True)
        #         full_response += token

        # for non-streaming use
        full_response = response.choices[0].message.content
        print(full_response)

        print()
        print("\nDone in", round(time.time() - start_time, 2), "seconds")

        if log: self.log_result(full_response, round(time.time() - start_time, 2))
        # log to conversation history 
        self.conversation_history_debug.append({
            "role": "user",
            "content": prompt
        })
        self.conversation_history_debug.append(
        {
            "role": "assistant",
            "content": full_response
        })

        return full_response
    
    def vllm_response(self, messages, response_format):
        response = client.chat.completions.create(
            model=self.LARGE_MODEL,
            messages=messages,
            #needs to escape invalid paths
            
            seed=44,
            response_format=response_format
        )
        return response

    def openwebui_response(self, messages):
        return requests.post(
            f"{OPENWEBUI_URL}/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": self.LARGE_MODEL,
                "messages": messages,
                "temperature": 0.0,
                "stream": False,
                "seed": 48,
                "top_p": 1.0,
                "top_k": 1.0,
                "repeat_penalty": 1.0,
                "mirostat": 0,
            },
            stream=False,
            timeout=200
        )
    
    def prompt_valid_DISARM_response(self, prompt, system_prompt):
        result_raw = self.prompt_llm_response(prompt, system_prompt)
        try:
            result_parsed = json.loads(result_raw)       
            parse_success = True         
        except json.JSONDecodeError:
            print("Error: Model Failed to return valid JSON")
        if self.valid_classifications(result_parsed):
            return result_parsed
        else: raise Exception("Error: Model failed to return valid classifications")

    def valid_classifications(self, json_results):

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
        if not all(v in self.available_classes for v in values):
            return False

        return True

    def log_result(self, result, time):
        self.log_to_file(f"\nResult:\n{result}\n\nTime: {time} seconds\n\n{'-'*50}\n\n")

    def log_round(self, result, time, attempts):
        self.log_to_file(f"ROUND SUMMARY:\nAvailable Classes:\n{self.available_classes}\n\nResult:\n{result}\n\nTime: {time} seconds\nFailures: {attempts}\n\n{'-'*50}\n\n")

    def log_final_result(self, total_tactics, total_techniques, time, do_analysis=False):
        self.log_to_file("EXECUTION SUMMARY:\nTotal Identified Tactics: {total_tactics}\nTotal Identified Techniques: {total_techniques}\n\nTotal execution time: {time}")
        if do_analysis:
            self.log_analysis()

    def log_to_file(self, message):
        with open(self.log_filename, "a", encoding="utf-8") as f:
            f.write(message)


    def log_analysis(self):
        # retrieve the execution log
        with open(self.log_filename, "r", encoding="utf-8") as f:
            execution_log = f.read()
            prompt = f"Provide a detailed anaysis of this execution log: \n\n {execution_log}"
            self.response_format=None
            analysis = self.prompt_llm_response(prompt=prompt, system_prompt=ANALYSIS_SYSTEM_PROMPT, log=False)
        with open(self.log_filename, "a", encoding="utf-8") as f:
            f.write(f"\n\nEXECUTION ANALYSIS:\n{analysis}")

    def log_debug(self, message):
        with open(self.log_filename, "a", encoding="utf-8") as f:
            f.write(f"\n\DEBUG:\n{message}")

    def new_log_file(self):
        timestamp = time.strftime("%Y%m%d-%H%M%S")
        self.log_filename = f".exe_logs/DISARM_log_{timestamp}.txt"
        with open(self.log_filename, "w", encoding="utf-8") as f:
            f.write(f"DISARM Log File - Created on {timestamp}\nSETUP:\nLarge Model: {self.LARGE_MODEL}\nTemperature: 0.0\n\n")
            
    def get_tactics(self):
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

        return filtered_tactics, available_classifications
    
    def identify_tactics(self):
        
        filtered_tactics, available_classifications = self.get_tactics()

        self.available_classes = available_classifications
        ta_format = {
            "type": "object",
            "properties": {
                "Tactics": {
                    "type": "array",
                    "items": {
                        "type": "string",
                        "enum": self.available_classes
                    }
                }
            },
            "required": ["Tactics"]
        }

        self.response_format={
            "type": "json_schema",
            "json_schema": {
                "name": "tactics_schema",
                "schema": ta_format
                }
            }
        # print(filtered_tactics)

        ta_prompt = f"""
{{
"Article": {json.dumps(self.article_content)},
"Tactics": {json.dumps(filtered_tactics, indent=2)}
}}
"""

        # print(ta_prompt)
        
        print("Identifying Tactics...")
        ta_result_parsed = self.prompt_valid_DISARM_response(prompt=ta_prompt, system_prompt=TA_SYSTEM_PROMPT)
        ta_result_list = ta_result_parsed.get("Tactics", [])    
        print("Identified Tactics: " + str(ta_result_list))
        return ta_result_list

    def identify_techniques_for_tactic(self, tactic):
        print("Testing for tactic: " + tactic)
        techniques = []
        for obj in self.disarm_json["objects"]:
            if obj.get("type") == "attack-pattern":
                for phase in obj.get("kill_chain_phases", []):
                    if phase.get("phase_name") == tactic:
                        techniques.append(obj)

        return self.identify_techniques(techniques)

    def identify_techniques(self, techniques=None, filter_ids=None):
        if techniques is None:
            techniques = self.get_all_techniques()

        filtered_techniques = []

        external_ids = []
        for technique in techniques:
            ex_id = get_mitre_external_id(technique)
            if filter_ids is None:
                filtered_techniques.append({
                    "external_id": ex_id,
                    "description": technique.get("description"),
                })
                external_ids.append(ex_id)
            elif ex_id in filter_ids:
                # filtering for use within reduced single clf in the ZeDPEB benchmark
                filtered_techniques.append({
                    "external_id": ex_id,
                    "description": technique.get("description"),
                })
                external_ids.append(ex_id)


        self.available_classes = external_ids

        t_format = {
            "type": "object",
            "properties": {
                "Techniques": {
                    "type": "array",
                    "items": {
                        "type": "string",
                        "enum": external_ids
                    }
                }
            },
            "required": ["Techniques"]
        }
        system_prompt = T_SYSTEM_PROMPT
        self.response_format={
                "type": "json_schema",
                "json_schema": {
                    "name": "techniques_schema",
                    "schema": t_format
                    }
                }
        
        t_prompt = f"""
{{
"Article": {json.dumps(self.article_content)},
"Techniques": {json.dumps(filtered_techniques, indent=2)}
}}
"""
                
        t_result_parsed = self.prompt_valid_DISARM_response(prompt=t_prompt, system_prompt=system_prompt)
        t_result_list = t_result_parsed.get("Techniques", [])
        print("Identified Techniques: " + str(t_result_list))
        return t_result_list
    
    def get_t_desc_from_id(self, external_ids):
        filtered_techniques = []
        for obj in self.disarm_json["objects"]:
            if obj.get("type") == "attack-pattern":
                for ref in obj.get("external_references", []):
                    if ref.get("source_name") == "mitre-attack":
                        if ref.get("external_id") in external_ids:
                            filtered_techniques.append({
                                "external_id": ref.get("external_id"),
                                "description": obj.get("description"),
                            })
        return filtered_techniques

    # TODO, fix for prompt overfitting by classifying article in batches
    def identify_rationales(self, external_ids, article_content=None):
        if article_content is None:
            article_content = self.article_content

        l = len(article_content)
        print(f"identifying rationales of article with length: {l}")

        # if the article is too large, it must be processed in batches with 1/3 overlap
        if l > 20000:
            print("Warning, article too large, splitting and extracting rationales in batches")
            split1 = article_content[0:int(l*0.65)]
            split2 = article_content[int(l*0.35):l-1]

            result_list = []
            result_list.extend(self.identify_rationales(external_ids, split1))
            result_list.extend(self.identify_rationales(external_ids, split2))

        else:
            filtered_techniques = self.get_t_desc_from_id(external_ids)

            t_format = {
                "type": "object",
                    "properties": {
                        "results": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties":{
                                    "technique": {
                                        "type": "string",
                                        "enum": external_ids
                                    },
                                    "rationales": {
                                        "type": "array",
                                        "items": {
                                            "type": "string"
                                        },
                                        "minItems": 1
                                    }
                                },
                                "required": ["technique", "rationales"]
                            },
                            "minItems": len(external_ids),
                            "maxItems": len(external_ids)
                        }
                    },
                    "required": ["results"]
            }
            system_prompt = T_RAT_SYSTEM_PROMPT
            
            self.response_format={
                    "type": "json_schema",
                    "json_schema": {
                        "name": "techniques_schema",
                        "schema": t_format
                        }
                    }
            
            t_prompt = f"""
    {{
    "Article": {json.dumps(article_content)},
    "Techniques": {json.dumps(filtered_techniques, indent=2)}
    }}
    """

            result_raw = self.prompt_llm_response(prompt=t_prompt, system_prompt=system_prompt)
            try:
                result_parsed = json.loads(result_raw)              
            except json.JSONDecodeError:
                print("Error: Model Failed to return valid JSON")

            result_list = [
                (item["technique"], item["rationales"])
                for item in result_parsed["results"]
            ]

            print("Result: " + str(result_list))
        return result_list

    def get_all_techniques(self):
        techniques = []
        for obj in self.disarm_json["objects"]:
            if obj.get("type") == "attack-pattern":
                techniques.append(obj)
        return techniques

    # MAIN EXECUTION
    def batch_clf(self, fast=False):
        start_time = time.time()

        #TACTICS
        if fast:
            tactics = self.identify_tactics()
        else:
            f, tactics = self.get_tactics()
        # reset conversation history for freshness
        # TODO change history reset to remove article from the prompt, and instead store as initial chat history
        self.conversation_history_main = []
        #TECHNIQUES LOOP
        total_techniques = []
        for tactic in tactics:
            techniques = self.identify_techniques_for_tactic(tactic)
            total_techniques.extend(techniques)

        print("Total Identified Techniques: " + str(total_techniques))
        print("\nTotal execution time: " + str(round(time.time() - start_time, 2)) + " seconds")
        self.log_final_result(tactics,total_techniques, round(time.time() - start_time, 2))
        return tactics, total_techniques

    def select_all_clf(self):
        start_time = time.time() 

        total_techniques = self.identify_techniques()

        print("Total Identified Techniques: " + str(total_techniques))
        print("\nTotal execution time: " + str(round(time.time() - start_time, 2)) + " seconds")
        self.log_final_result(None,total_techniques, round(time.time() - start_time, 2))
        return total_techniques

    def single_clf(self):
        start_time = time.time() 
        available_techniques = self.get_all_techniques()
        total_techniques = []
        for technique in available_techniques:
            total_techniques += self.identify_techniques(techniques=[technique])

        print("Total Identified Techniques: " + str(total_techniques))
        print("\nTotal execution time: " + str(round(time.time() - start_time, 2)) + " seconds")
        self.log_final_result(None,total_techniques, round(time.time() - start_time, 2))
        return total_techniques

def get_mitre_external_id(obj):
    for ref in obj.get("external_references", []):
        if ref.get("source_name") == "mitre-attack":
            return ref.get("external_id")
    return None

def main():
    interpreter = DISARMClassifier()
    # interpreter.batch_clf(fast=False)
    interpreter.identify_rationales(["T0023", "T0085.003"])

if __name__ == "__main__":
    main()