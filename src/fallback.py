"""
Offline fallback dictionary for WordBuddy.
Used when the LLM is unavailable or returns an invalid response.
Each entry matches the 7-key schema returned by src/llm.py.
Definitions are written at a 2nd–3rd grade reading level.
"""

from __future__ import annotations

FALLBACK_DICT: dict[str, dict] = {
    # ------------------------------------------------------------------ A
    "ancient": {
        "syllables": "an·cient",
        "pronunciation_hint": "AYN-shent",
        "definition": "Very, very old — from a long, long time ago.",
        "examples": [
            "The ancient castle had been standing for over a thousand years.",
            "Scientists found ancient bones buried deep in the ground.",
        ],
        "analogy": "If your grandparent is old, ancient is like your grandparent times a million!",
        "encouragement": "You just learned a word that historians use every day. Amazing!",
        "practice_question": "What is the most ancient thing you have ever seen or heard about?",
    },
    # ------------------------------------------------------------------ C
    "circumference": {
        "syllables": "cir·cum·fer·ence",
        "pronunciation_hint": "ser-KUM-fer-ents",
        "definition": "The distance all the way around the outside of a circle.",
        "examples": [
            "We measured the circumference of the basketball with a piece of string.",
            "The circumference of the Earth is almost 25,000 miles.",
        ],
        "analogy": "It is like putting a belt around a round tree trunk — the length of that belt is the circumference.",
        "encouragement": "That is a big math word and you looked it up. You are a star!",
        "practice_question": "Can you find something round and try to measure its circumference with string?",
    },
    "collaborate": {
        "syllables": "col·lab·o·rate",
        "pronunciation_hint": "kuh-LAB-uh-rayt",
        "definition": "To work together with other people to make something happen.",
        "examples": [
            "The students collaborated on a poster about ocean animals.",
            "The two chefs collaborated to create the most delicious dessert ever.",
        ],
        "analogy": "It is like when you and a friend build a LEGO set together — two people, one awesome creation!",
        "encouragement": "You collaborated with your brain today and learned something new. Team effort!",
        "practice_question": "Who is someone you like to collaborate with, and what do you make together?",
    },
    "constitution": {
        "syllables": "con·sti·tu·tion",
        "pronunciation_hint": "kon-stih-TOO-shun",
        "definition": "A set of rules that says how a country or group is run.",
        "examples": [
            "The United States Constitution tells us the rights every person has.",
            "Our school's student council wrote a short constitution for their club.",
        ],
        "analogy": "It is like the rule book for a board game, except it is the rule book for a whole country.",
        "encouragement": "Learning words like 'constitution' makes you a great future citizen. Bravo!",
        "practice_question": "What is one rule you would put in a constitution for your classroom?",
    },
    # ------------------------------------------------------------------ E
    "enormous": {
        "syllables": "e·nor·mous",
        "pronunciation_hint": "ee-NOR-mus",
        "definition": "Really, really big — much bigger than usual.",
        "examples": [
            "The enormous elephant could barely fit through the gate.",
            "She took an enormous bite of her birthday cake.",
        ],
        "analogy": "It is like if your backpack grew as big as your whole bedroom!",
        "encouragement": "Wow — 'enormous' is a HUGE word for a huge idea. You have got this!",
        "practice_question": "Can you think of something enormous that you have seen?",
    },
    "environment": {
        "syllables": "en·vi·ron·ment",
        "pronunciation_hint": "en-VY-run-ment",
        "definition": "All the living things and places around us, like forests, oceans, and air.",
        "examples": [
            "Picking up litter helps protect the environment.",
            "Different animals need different environments to stay healthy.",
        ],
        "analogy": "Your bedroom is your personal environment — the environment outside is the bedroom for all living things.",
        "encouragement": "People who care about the environment are called scientists AND heroes. Just like you!",
        "practice_question": "What is one thing you can do today to help the environment?",
    },
    "evidence": {
        "syllables": "ev·i·dence",
        "pronunciation_hint": "EV-ih-dents",
        "definition": "Facts or clues that help show whether something is true.",
        "examples": [
            "The muddy footprints were evidence that someone had walked through the garden.",
            "Scientists look for evidence before they say something is true.",
        ],
        "analogy": "Evidence is like puzzle pieces that help you see the full picture of what really happened.",
        "encouragement": "Detectives use evidence every day — and now you know the word they use. Super cool!",
        "practice_question": "Can you think of a time when you used evidence to figure something out?",
    },
    "exaggerate": {
        "syllables": "ex·ag·ger·ate",
        "pronunciation_hint": "eg-ZAJ-er-ayt",
        "definition": "To make something sound bigger, worse, or more exciting than it really is.",
        "examples": [
            "He was exaggerating when he said he waited a million years for lunch.",
            "My sister always exaggerates — she said her backpack weighed a ton!",
        ],
        "analogy": "Exaggerating is like using a magnifying glass on a story to make every part look giant.",
        "encouragement": "You learned a word that writers use all the time. Your vocabulary is growing fast!",
        "practice_question": "Can you make up a funny sentence that exaggerates something you did today?",
    },
    "exhausted": {
        "syllables": "ex·haust·ed",
        "pronunciation_hint": "eg-ZAWST-ed",
        "definition": "So tired that you feel like you have no energy left at all.",
        "examples": [
            "After running the whole race, Jaylen was completely exhausted.",
            "The exhausted puppy fell asleep as soon as it sat down.",
        ],
        "analogy": "It is like your body is a phone with 1% battery left — barely anything to keep going!",
        "encouragement": "Learning new words is hard work, but you are doing amazingly!",
        "practice_question": "When is the last time you felt exhausted? What were you doing?",
    },
    # ------------------------------------------------------------------ F
    "ferocious": {
        "syllables": "fe·ro·cious",
        "pronunciation_hint": "feh-ROH-shus",
        "definition": "Very fierce, wild, and a little scary.",
        "examples": [
            "The ferocious lion roared so loud the whole savanna shook.",
            "The puppy gave a ferocious bark, but it just wanted to play.",
        ],
        "analogy": "Think of how a thunderstorm sounds — loud, powerful, and hard to ignore. That is ferocious!",
        "encouragement": "Learning ferocious words makes your vocabulary ferociously strong!",
        "practice_question": "Can you roar as ferociously as a lion? Give it a try!",
    },
    "fossil": {
        "syllables": "fos·sil",
        "pronunciation_hint": "FAH-sul",
        "definition": "The hardened remains or shape of a plant or animal that lived a very long time ago.",
        "examples": [
            "The museum had a fossil of a dinosaur bone that was 65 million years old.",
            "She found a small fossil of a shell while hiking near the lake.",
        ],
        "analogy": "A fossil is like a photograph in rock — it shows us what life looked like millions of years ago.",
        "encouragement": "You are learning science words that real paleontologists use. Keep going!",
        "practice_question": "If you could find any fossil in the world, which creature would you want it to be from?",
    },
    # ------------------------------------------------------------------ G
    "government": {
        "syllables": "gov·ern·ment",
        "pronunciation_hint": "GUV-ern-ment",
        "definition": "The group of people in charge of running a city, state, or country.",
        "examples": [
            "The government builds roads and schools for people to use.",
            "Citizens vote to choose who will be in the government.",
        ],
        "analogy": "A government is like the teachers and principal of a school, except they are in charge of a whole place instead.",
        "encouragement": "Big thinkers learn about government — and that is exactly what you are doing!",
        "practice_question": "What is one thing you think a good government should do for people?",
    },
    # ------------------------------------------------------------------ H
    "hesitate": {
        "syllables": "hes·i·tate",
        "pronunciation_hint": "HEZ-ih-tayt",
        "definition": "To pause for a moment because you are not sure what to do.",
        "examples": [
            "She hesitated at the top of the diving board before jumping in.",
            "He hesitated before answering because he wanted to think carefully.",
        ],
        "analogy": "Hesitating is like pressing pause on a movie — everything stops for just a second.",
        "encouragement": "Even hesitating to look up a word is brave. You did it anyway. Nice work!",
        "practice_question": "Can you think of a time when you hesitated before doing something?",
    },
    "hypothesis": {
        "syllables": "hy·poth·e·sis",
        "pronunciation_hint": "hy-POTH-eh-sis",
        "definition": "A smart guess that you then test to see if it is true.",
        "examples": [
            "Her hypothesis was that plants grow faster in sunlight, so she set up an experiment.",
            "The scientist wrote down his hypothesis before starting the test.",
        ],
        "analogy": "A hypothesis is like saying 'I think the cookie is in the jar' before you look inside — it is your best guess.",
        "encouragement": "Scientists use this word every single day. You are thinking like one right now!",
        "practice_question": "What is a hypothesis you could test about something in your home or school?",
    },
    # ------------------------------------------------------------------ I
    "illuminate": {
        "syllables": "il·lu·mi·nate",
        "pronunciation_hint": "ih-LOO-mih-nayt",
        "definition": "To light something up, or to help make an idea clearer.",
        "examples": [
            "The candles illuminated the whole room with a warm glow.",
            "The teacher's example illuminated the math problem for everyone.",
        ],
        "analogy": "Illuminate is like turning on a torch in a dark room — suddenly you can see everything!",
        "encouragement": "You are illuminating your brain with new words. That is really something special!",
        "practice_question": "Can you think of something that illuminates a room in your home?",
    },
    # ------------------------------------------------------------------ M
    "magnificent": {
        "syllables": "mag·nif·i·cent",
        "pronunciation_hint": "mag-NIF-ih-sent",
        "definition": "So beautiful or wonderful that it takes your breath away.",
        "examples": [
            "The sunset over the ocean was truly magnificent.",
            "The circus performer did a magnificent backflip on the tightrope.",
        ],
        "analogy": "You know that feeling when you see fireworks light up the whole sky? That is magnificent!",
        "encouragement": "You are doing a magnificent job learning new words today!",
        "practice_question": "What is the most magnificent thing you have ever seen?",
    },
    "metamorphosis": {
        "syllables": "met·a·mor·pho·sis",
        "pronunciation_hint": "met-ah-MOR-foh-sis",
        "definition": "A big change in the shape or form of a living thing as it grows.",
        "examples": [
            "The metamorphosis of a caterpillar into a butterfly takes about two weeks.",
            "We watched the metamorphosis of a tadpole into a frog in our classroom tank.",
        ],
        "analogy": "It is like when a lump of plain dough goes into the oven and comes out as a beautiful loaf of bread — completely changed!",
        "encouragement": "You just learned one of the coolest science words there is. You should be proud!",
        "practice_question": "Can you name another animal that goes through a metamorphosis?",
    },
    # ------------------------------------------------------------------ N
    "necessary": {
        "syllables": "nec·es·sar·y",
        "pronunciation_hint": "NES-eh-sair-ee",
        "definition": "Something that must happen or must be there — you cannot do without it.",
        "examples": [
            "Water is necessary for all living things to survive.",
            "It is necessary to wear a helmet when riding a bike.",
        ],
        "analogy": "Necessary is like a key — without it, the door simply will not open.",
        "encouragement": "Learning is necessary for a great future — and you are already doing it!",
        "practice_question": "What is one thing that is necessary for you to have a good day at school?",
    },
    # ------------------------------------------------------------------ O
    "obvious": {
        "syllables": "ob·vi·ous",
        "pronunciation_hint": "OB-vee-us",
        "definition": "Easy to see or understand — it is right there in front of you.",
        "examples": [
            "It was obvious that the dog had eaten the cake because there was frosting on his nose.",
            "The answer to the first question was obvious to everyone in the class.",
        ],
        "analogy": "Obvious is like finding your shoes right in the middle of the floor — you can not miss them!",
        "encouragement": "It is obvious that you love learning. Keep going — you are doing great!",
        "practice_question": "Can you think of something that is obvious to you but might not be obvious to a baby?",
    },
    # ------------------------------------------------------------------ P
    "peculiar": {
        "syllables": "pe·cu·li·ar",
        "pronunciation_hint": "peh-KYOO-lee-er",
        "definition": "Strange or unusual in a way that makes you look twice.",
        "examples": [
            "The peculiar smell coming from the science room made everyone curious.",
            "My cat has a peculiar habit of sleeping inside her food bowl.",
        ],
        "analogy": "It is like finding a purple banana — it is a banana, but something is definitely different!",
        "encouragement": "You just learned a peculiar word — and that makes YOU pretty awesome!",
        "practice_question": "What is the most peculiar thing you have ever seen or heard?",
    },
    "persistent": {
        "syllables": "per·sis·tent",
        "pronunciation_hint": "per-SIS-tent",
        "definition": "Keeps trying and does not give up, even when things are hard.",
        "examples": [
            "The persistent ant kept carrying crumbs back to its hill even in the rain.",
            "She was persistent about learning to ride her bike until she finally got it.",
        ],
        "analogy": "Being persistent is like a dripping tap — it just keeps going and going until the job is done.",
        "encouragement": "Looking up hard words shows you are persistent — and that is a superpower!",
        "practice_question": "What is something hard that you have been persistent about?",
    },
    "photosynthesis": {
        "syllables": "pho·to·syn·the·sis",
        "pronunciation_hint": "foh-toh-SIN-theh-sis",
        "definition": "The way green plants use sunlight to make their own food from air and water.",
        "examples": [
            "Without photosynthesis, plants could not grow and we would have no oxygen.",
            "Leaves are green because they are full of the stuff that makes photosynthesis happen.",
        ],
        "analogy": "Photosynthesis is like a plant's kitchen — sunlight is the stove and the leaves are the chefs.",
        "encouragement": "That is one of the biggest words in science class and YOU looked it up. You are a rock star!",
        "practice_question": "Can you explain photosynthesis to someone in your house using only simple words?",
    },
    # ------------------------------------------------------------------ R
    "reluctant": {
        "syllables": "re·luc·tant",
        "pronunciation_hint": "reh-LUK-tent",
        "definition": "Not really wanting to do something, even if you do it anyway.",
        "examples": [
            "She was reluctant to eat her broccoli, but she did it for dessert.",
            "The reluctant puppy slowly walked toward the bathtub.",
        ],
        "analogy": "It is like when you have to turn off your game — you do it, but you really do not want to!",
        "encouragement": "Even if you were a little reluctant at first, you learned a brand new word. That is brave!",
        "practice_question": "What is something you feel reluctant about but you do anyway?",
    },
    # ------------------------------------------------------------------ S
    "sufficient": {
        "syllables": "suf·fi·cient",
        "pronunciation_hint": "suh-FISH-ent",
        "definition": "Enough — just the right amount to meet a need.",
        "examples": [
            "She had sufficient time to finish the test before the bell rang.",
            "Make sure you drink sufficient water on a hot day.",
        ],
        "analogy": "Sufficient is like filling your water bottle just enough so it does not overflow but does not run dry.",
        "encouragement": "You are more than sufficient at learning new words — you are excellent!",
        "practice_question": "Can you think of a time when you had just sufficient time to finish something?",
    },
    "suspicious": {
        "syllables": "sus·pi·cious",
        "pronunciation_hint": "suh-SPISH-us",
        "definition": "Having a feeling that something is not quite right or that someone is hiding something.",
        "examples": [
            "The detective was suspicious when the jar of cookies was empty but no one admitted eating them.",
            "My dog looked suspicious when he walked in with muddy paws.",
        ],
        "analogy": "It is like when your friend is smiling too much right before your birthday — something is going on!",
        "encouragement": "You are one smart cookie for adding this word to your collection!",
        "practice_question": "Has something ever seemed suspicious to you? What happened?",
    },
    # ------------------------------------------------------------------ T
    "territory": {
        "syllables": "ter·ri·to·ry",
        "pronunciation_hint": "TAIR-ih-tor-ee",
        "definition": "An area of land that belongs to or is controlled by someone.",
        "examples": [
            "The lion walked around the edge of its territory to warn other animals away.",
            "Alaska became a United States territory before it became a state.",
        ],
        "analogy": "A territory is like your own bedroom — it is your space, and you know where the edges are.",
        "encouragement": "Geography words like territory make your brain grow in every direction. Keep it up!",
        "practice_question": "If you had your own territory, what would you have inside it?",
    },
    "transparent": {
        "syllables": "trans·par·ent",
        "pronunciation_hint": "trans-PAIR-ent",
        "definition": "So clear you can see right through it, like glass.",
        "examples": [
            "The fish tank was transparent so we could watch all the fish swim.",
            "She wrapped the cookies in transparent plastic so everyone could see them.",
        ],
        "analogy": "It is like looking through a clean window — you can see everything on the other side!",
        "encouragement": "You can clearly see how smart you are for learning this word!",
        "practice_question": "Can you name three things in your house that are transparent?",
    },
    "tremendous": {
        "syllables": "tre·men·dous",
        "pronunciation_hint": "treh-MEN-dus",
        "definition": "Very great, very large, or very impressive.",
        "examples": [
            "The crowd made a tremendous noise when the team scored the winning goal.",
            "She put in a tremendous amount of work on her science project.",
        ],
        "analogy": "Tremendous is like enormous's louder, more exciting cousin — everything is bigger and bolder!",
        "encouragement": "You are making tremendous progress with your vocabulary today!",
        "practice_question": "What is something you have done recently that took tremendous effort?",
    },
    # ------------------------------------------------------------------ U
    "unfamiliar": {
        "syllables": "un·fa·mil·iar",
        "pronunciation_hint": "un-fah-MIL-ee-er",
        "definition": "Something you have not seen or heard before — it feels new and strange.",
        "examples": [
            "The unfamiliar sound outside woke the dog up in the middle of the night.",
            "On the first day of school, everything felt unfamiliar.",
        ],
        "analogy": "Unfamiliar is like walking into a new place for the first time — you are not sure what is where yet.",
        "encouragement": "Every word you look up becomes less unfamiliar. You are growing every day!",
        "practice_question": "What is something that felt unfamiliar at first but feels normal to you now?",
    },
    # ------------------------------------------------------------------ V
    "vocabulary": {
        "syllables": "vo·cab·u·lar·y",
        "pronunciation_hint": "voh-KAB-yoo-lair-ee",
        "definition": "All the words a person knows and can use.",
        "examples": [
            "Reading every day helps you build a bigger vocabulary.",
            "Her vocabulary was so strong she could explain anything clearly.",
        ],
        "analogy": "Your vocabulary is like a toolbox — the more words you have, the more you can build and say!",
        "encouragement": "Every word you learn makes your vocabulary bigger and YOUR mind stronger!",
        "practice_question": "What is your favourite word in your vocabulary right now?",
    },
    # ------------------------------------------------------------------ W
    "wonderful": {
        "syllables": "won·der·ful",
        "pronunciation_hint": "WUN-der-ful",
        "definition": "Something that makes you feel happy, amazed, or full of wonder.",
        "examples": [
            "The view from the top of the hill was absolutely wonderful.",
            "She got a wonderful surprise on her birthday.",
        ],
        "analogy": "Wonderful is like the feeling you get on the first day of summer — warm, happy, and full of possibility.",
        "encouragement": "You are doing a wonderful job learning today. Never stop!",
        "practice_question": "What is one wonderful thing that happened to you this week?",
    },
}

# Generic response when the word is not in FALLBACK_DICT
GENERIC_FALLBACK: dict = {
    "syllables": "?",
    "pronunciation_hint": "ask a grown-up to help you say it",
    "definition": "That is a tricky one! We do not have it in our word list yet.",
    "examples": [
        "Try looking it up in a dictionary with a grown-up.",
        "You could also ask your teacher what it means.",
    ],
    "analogy": "Every word is like a little mystery waiting to be solved!",
    "encouragement": "You are so brave for asking about a word you did not know. Keep it up!",
    "practice_question": "Can you find this word in a book or ask someone what it means?",
}


def lookup(word: str) -> dict:
    """Return a schema-compliant dict for the given word.

    Tries exact match first, then case-insensitive + stripped match.
    Falls back to GENERIC_FALLBACK if the word is not in the dictionary.
    """
    if word in FALLBACK_DICT:
        return FALLBACK_DICT[word]
    lower = word.lower().strip()
    if lower in FALLBACK_DICT:
        return FALLBACK_DICT[lower]
    return GENERIC_FALLBACK
