"""
week3/chatbot.py - Smart Farm Full CLI Chatbot (Week 3)
========================================================
The main entry point for the Smart Farm AI Assistant.

Wires together the full NLP pipeline:
  Week 1 -> Tokenization, stop word removal, stemming, lemmatization
  Week 2 -> POS tagging, noun/verb extraction
  Week 3 -> HMM entity sequence labeling
  KB     -> Knowledge base lookup for solutions

Usage:
  python week3/chatbot.py           - text mode
  python week3/chatbot.py --speech  - speech input mode

Course: BIT4133 Natural Language Processing - Week 3
Project: Smart Farm AI Assistant
"""

import sys
import os
import argparse

# -- Path setup ----------------------------------------------------------------
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
sys.path.insert(0, os.path.join(ROOT, "week1"))
sys.path.insert(0, os.path.join(ROOT, "week2"))
sys.path.insert(0, os.path.join(ROOT, "week3"))

# -- Imports -------------------------------------------------------------------
from nlp_pipeline  import run_full_pipeline
from pos_tagger    import analyse_farmer_query
from hmm_entity    import FarmingHMM, print_labeled_sentence, print_entities
from speech_input  import get_speech_input, check_speech_dependencies
from knowledge_base import lookup_solution, CROP_VOCAB, SYMPTOM_VOCAB, DISEASE_VOCAB

# -- Colorama for Windows terminal colors --------------------------------------
try:
    from colorama import init, Fore, Style
    init(autoreset=True)
    COLOR = True
except ImportError:
    COLOR = False
    class Fore:
        GREEN = YELLOW = CYAN = RED = MAGENTA = WHITE = BLUE = ""
    class Style:
        BRIGHT = RESET_ALL = DIM = ""


# =============================================================================
# CHATBOT ENGINE
# =============================================================================

class SmartFarmChatbot:
    """
    Smart Farm AI Chatbot - processes farmer queries through the full NLP pipeline
    and returns farming solutions from the knowledge base.
    """

    BANNER = r"""
  +==============================================================+
  |          🌾  SMART FARM AI ASSISTANT  🌾                    |
  |     Powered by NLP - BIT4133 Course Project                  |
  |     Type your farming problem or press 'q' to quit           |
  +==============================================================+
    """

    HELP_TEXT = """
  Commands:
    Type any farming problem (e.g. "my maize is turning yellow")
    help    - Show this help message
    crops   - List all known crops in the knowledge base
    q/quit  - Exit the chatbot
    """

    KNOWN_CROPS = sorted(set(CROP_VOCAB))

    def __init__(self, speech_mode: bool = False, verbose: bool = True):
        self.speech_mode = speech_mode
        self.verbose     = verbose
        self.hmm         = FarmingHMM()
        self.session_count = 0

    # -- Input -------------------------------------------------------------
    def get_input(self) -> str:
        """Get input from keyboard or microphone depending on mode."""
        if self.speech_mode:
            print(f"\n{Fore.CYAN}  🎤 Speak your farming problem (or press Enter to type):{Style.RESET_ALL}")
            text = get_speech_input(timeout=6, phrase_limit=12)
            if not text:
                print(f"  {Fore.YELLOW}No speech detected - switching to text input.{Style.RESET_ALL}")
                text = input(f"\n  {Fore.GREEN}Farmer (type): {Style.RESET_ALL}").strip()
        else:
            text = input(f"\n  {Fore.GREEN}Farmer: {Style.RESET_ALL}").strip()
        return text

    # -- Pipeline ----------------------------------------------------------
    def _run_week1_pipeline(self, text: str) -> dict:
        """Run Week 1 tokenization pipeline."""
        return run_full_pipeline(text, verbose=False)

    def _run_week2_analysis(self, text: str) -> dict:
        """Run Week 2 POS tagging and role classification."""
        return analyse_farmer_query(text, verbose=False)

    def _run_week3_hmm(self, text: str) -> tuple:
        """Run Week 3 HMM entity extraction."""
        labeled  = self.hmm.label_sentence(text)
        entities = self.hmm.extract_entities(text)
        return labeled, entities

    # -- Knowledge base lookup ---------------------------------------------
    def _find_solution(self, entities: dict, pos_result: dict, w1: dict) -> dict:
        """
        Look up the most appropriate solution from the knowledge base.

        Priority:
          1. Exact (crop, disease/symptom) match from HMM entities
          2. POS farming roles (crop + symptom keyword)
          3. Keyword scan of Week 1 filtered tokens
        """
        # Gather crop candidates
        crops = entities.get("CROP", []) + pos_result["farming_roles"].get("crops", [])
        # Gather symptom candidates from HMM + POS
        symptoms = (
            entities.get("SYMPTOM", []) +
            entities.get("DISEASE", []) +
            pos_result["farming_roles"].get("symptoms", [])
        )

        # Unique, preserve order
        def dedup(lst):
            seen, result = set(), []
            for x in lst:
                if x not in seen:
                    seen.add(x)
                    result.append(x)
            return result

        crops    = dedup(crops)
        symptoms = dedup(symptoms)

        # Try each crop + symptom combination
        for crop in crops:
            for symptom in symptoms:
                result = lookup_solution(crop, symptom)
                if "consult" not in result["solution"].lower():
                    return result, crop, symptom

        # Try crop + Week-1 filtered token fallback
        for crop in crops:
            for word in w1.get("filtered", []):
                result = lookup_solution(crop, word)
                if "consult" not in result["solution"].lower():
                    return result, crop, word

        # Fallback
        crop_str    = crops[0]    if crops    else "your crop"
        symptom_str = symptoms[0] if symptoms else "the issue"
        return lookup_solution(crop_str, symptom_str), crop_str, symptom_str

    # -- Display -----------------------------------------------------------
    def _display_pipeline(self, w1: dict, w2: dict, labeled: list, entities: dict):
        """Display the NLP pipeline steps."""
        print(f"\n  {Fore.CYAN}{'-'*60}")
        print(f"  📊 NLP PIPELINE ANALYSIS")
        print(f"  {'-'*60}{Style.RESET_ALL}")

        # Week 1
        print(f"\n  {Fore.YELLOW}[WEEK 1 - Tokenization & Text Normalization]{Style.RESET_ALL}")
        print(f"  Tokens   : {w1['tokens']}")
        print(f"  Filtered : {w1['filtered']}  (stopwords removed)")
        print(f"  Stems    : {w1['stems']}     (Porter stemming)")
        print(f"  Lemmas   : {w1['lemmas']}    (WordNet lemmatization)")

        # Week 2
        roles = w2["farming_roles"]
        print(f"\n  {Fore.YELLOW}[WEEK 2 - POS Tagging & Role Classification]{Style.RESET_ALL}")
        print(f"  POS Tags : {[(w, t) for w, t in w2['tagged'] if t not in ('DT','IN','PRP','PRP$','CC')]}")
        print(f"  Nouns    : {[w for w, _ in w2['nouns']]}")
        print(f"  Verbs    : {[w for w, _ in w2['verbs']]}")
        print(f"  NP chunks: {w2['noun_phrases']}")
        print(f"  Crops ↓  : {roles['crops']}    Symptoms ↓: {roles['symptoms']}")

        # Week 3
        print(f"\n  {Fore.YELLOW}[WEEK 3 - HMM Sequence Labeling]{Style.RESET_ALL}")
        print(f"  Labeled  :", end=" ")
        for word, label in labeled:
            if label != "O":
                print(f"[{word}/{label}]", end=" ")
            else:
                print(word, end=" ")
        print()
        print(f"  Entities :")
        for ent_type in ["CROP", "DISEASE", "SYMPTOM", "LOCATION", "ACTION"]:
            vals = entities.get(ent_type, [])
            if vals:
                print(f"    {ent_type:<10}: {', '.join(vals)}")

    def _display_solution(self, solution: dict, crop: str, symptom: str):
        """Display the farming solution."""
        severity_colors = {
            "critical": Fore.RED,
            "high":     Fore.RED,
            "medium":   Fore.YELLOW,
            "low":      Fore.GREEN,
            "unknown":  Fore.WHITE,
            "varies":   Fore.CYAN,
        }
        sev   = solution.get("severity", "unknown")
        color = severity_colors.get(sev, Fore.WHITE)

        print(f"\n  {Fore.GREEN}{'='*60}")
        print(f"  💡 SMART FARM SOLUTION")
        print(f"  {'='*60}{Style.RESET_ALL}")
        print(f"\n  {Fore.CYAN}Identified:  {Style.BRIGHT}{crop.upper()} - {symptom}{Style.RESET_ALL}")
        print(f"  {color}Severity  : {sev.upper()}{Style.RESET_ALL}")
        print(f"\n  {Fore.WHITE}Cause:{Style.RESET_ALL}")
        print(f"  {solution['cause']}")
        print(f"\n  {Fore.GREEN}Solution:{Style.RESET_ALL}")
        # Word-wrap the solution
        words = solution["solution"].split()
        line, line_len = "  ", 0
        for word in words:
            if line_len + len(word) + 1 > 70:
                print(line)
                line, line_len = "  ", 0
            line     += word + " "
            line_len += len(word) + 1
        if line.strip():
            print(line)
        print(f"\n  {Fore.YELLOW}Recommended Action(s):{Style.RESET_ALL}")
        for action in solution["action"].split("|"):
            print(f"  + {action.strip()}")

    # -- Main processing ---------------------------------------------------
    def process_query(self, query: str) -> bool:
        """
        Process a single farmer query through the full NLP pipeline.

        Returns:
            False if the user wants to quit, True otherwise.
        """
        query = query.strip()

        # -- Commands ------------------------------------------------------
        if query.lower() in ("q", "quit", "exit", "bye"):
            print(f"\n  {Fore.CYAN}Thank you for using Smart Farm AI! Happy farming! 🌾{Style.RESET_ALL}\n")
            return False

        if query.lower() in ("help", "?", "h"):
            print(self.HELP_TEXT)
            return True

        if query.lower() == "crops":
            print(f"\n  Known crops: {', '.join(self.KNOWN_CROPS)}")
            return True

        if not query:
            print(f"  {Fore.YELLOW}Please type or speak a farming problem.{Style.RESET_ALL}")
            return True

        self.session_count += 1
        print(f"\n  {Fore.CYAN}Processing your query...{Style.RESET_ALL}")

        # -- Run full NLP pipeline -----------------------------------------
        w1      = self._run_week1_pipeline(query)
        w2      = self._run_week2_analysis(query)
        labeled, entities = self._run_week3_hmm(query)

        # -- Display pipeline (verbose mode) -------------------------------
        if self.verbose:
            self._display_pipeline(w1, w2, labeled, entities)

        # -- Look up solution ----------------------------------------------
        solution, crop, symptom = self._find_solution(entities, w2, w1)
        self._display_solution(solution, crop, symptom)

        print()
        return True

    # -- Chat loop ---------------------------------------------------------
    def run(self):
        """Start the interactive chatbot loop."""
        print(Fore.GREEN + self.BANNER + Style.RESET_ALL)

        if self.speech_mode:
            if check_speech_dependencies():
                print(f"  {Fore.GREEN}✅ Speech recognition enabled.{Style.RESET_ALL}")
            else:
                print(f"  {Fore.YELLOW}⚠  Speech libraries not available - using text mode.{Style.RESET_ALL}")
                self.speech_mode = False

        print(f"  {Fore.CYAN}Type 'help' for commands. Type 'q' to quit.{Style.RESET_ALL}")
        print(f"  Example: \"My maize leaves are turning yellow\"\n")

        while True:
            try:
                query = self.get_input()
                if not self.process_query(query):
                    break
            except (KeyboardInterrupt, EOFError):
                print(f"\n\n  {Fore.CYAN}Exiting Smart Farm. Goodbye! 🌾{Style.RESET_ALL}\n")
                break


# =============================================================================
# ENTRY POINT
# =============================================================================

def main():
    parser = argparse.ArgumentParser(
        description="Smart Farm AI Chatbot - NLP-powered farming assistant"
    )
    parser.add_argument(
        "--speech",
        action="store_true",
        default=False,
        help="Enable speech input mode (requires SpeechRecognition + PyAudio)"
    )
    parser.add_argument(
        "--quiet",
        action="store_true",
        default=False,
        help="Suppress NLP pipeline display (show only solutions)"
    )
    parser.add_argument(
        "--demo",
        action="store_true",
        default=False,
        help="Run a non-interactive demonstration with preset queries"
    )
    args = parser.parse_args()

    chatbot = SmartFarmChatbot(
        speech_mode=args.speech,
        verbose=not args.quiet
    )

    if args.demo:
        import time
        # Non-interactive demo mode for screenshots / testing
        print(Fore.GREEN + chatbot.BANNER + Style.RESET_ALL)
        demo_queries = [
            "My maize leaves are turning yellow",
            "The tomato plants have blight",
            "My potato crop is wilting after heavy rain",
            "I see rust on my bean leaves",
            "How do I control cassava mosaic disease?",
        ]
        print(f"  {Fore.CYAN}=== DEMO MODE - {len(demo_queries)} preset queries ==={Style.RESET_ALL}\n")
        for i, q in enumerate(demo_queries, 1):
            print(f"\n  {Fore.GREEN}Farmer: {q}{Style.RESET_ALL}")
            chatbot.process_query(q)
            if i < len(demo_queries):
                print(f"  {Fore.CYAN}--- next query in 1 second ---{Style.RESET_ALL}")
                time.sleep(1)
        print(f"\n  {Fore.GREEN}Demo complete. All {len(demo_queries)} queries processed. 🌾{Style.RESET_ALL}\n")
    else:
        chatbot.run()


if __name__ == "__main__":
    main()
