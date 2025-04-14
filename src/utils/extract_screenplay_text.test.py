import unittest

from extract_screenplay_text import extract_screenplay_text

input_text = """
Got it! Here's a draft of that scene.

===
**INT. THE GEEK TAVERN - NIGHT**

The dimly lit bar is filled with chatter and soft music. NERDS in various fandom t-shirts are scattered around. At a corner table, ERIC (late 20s, wearing a "Pythonista" shirt) and KYLE (late 20s, sporting a "Java Forever" hat) have their laptops open, beers untouched.

**ERIC**
It's tabs, Kyle. One tap, perfect alignment. You can't argue with efficiency.

**KYLE**
(rolling his eyes)
Efficiency doesn't mean quality, Eric. Four spaces, always consistent. That's real control.

ERIC leans in, intense.

**ERIC**
You're just asking for chaos when your code merges, man. Tabs adapt to the environment.

**KYLE**
(louder, gesturing wildly)
No way! Spaces ensure that chaos never happens. Predictable formatting, every time.

Nearby PATRONS start to notice the growing argument. A couple of them chuckle, while others are visibly curious.

ERIC stands up, eyes locked with KYLE.

**ERIC**
It's about flexibility, Kyle. You're too rigid!

KYLE stands as well, matching Eric's stance.

**KYLE**
And you're too loose with your principles!

The BARTENDER (50s, with a thick beard and a worn "Peacekeeper" apron) notices the tension rising and steps over.

**BARTENDER**
Hey, fellas, calm down. Code wars aren't worth a scene.

ERIC and KYLE exchange looks, a tense silence lingers before they reluctantly sit back down.

**ERIC**
(sighing)
Maybe... we could agree to disagree?

**KYLE**
(grumbling)
Fine. But four spaces are objectively better.

ERIC chuckles, taking a swig of his beer.

**ERIC**
We'll see about that.

The tension eases as they return to their laptops, their argument a new chapter in their ongoing friendship.

===

Would you like to make any changes or updates to this scene?
"""

expected_text = """**INT. THE GEEK TAVERN - NIGHT**

The dimly lit bar is filled with chatter and soft music. NERDS in various fandom t-shirts are scattered around. At a corner table, ERIC (late 20s, wearing a "Pythonista" shirt) and KYLE (late 20s, sporting a "Java Forever" hat) have their laptops open, beers untouched.

**ERIC**
It's tabs, Kyle. One tap, perfect alignment. You can't argue with efficiency.

**KYLE**
(rolling his eyes)
Efficiency doesn't mean quality, Eric. Four spaces, always consistent. That's real control.

ERIC leans in, intense.

**ERIC**
You're just asking for chaos when your code merges, man. Tabs adapt to the environment.

**KYLE**
(louder, gesturing wildly)
No way! Spaces ensure that chaos never happens. Predictable formatting, every time.

Nearby PATRONS start to notice the growing argument. A couple of them chuckle, while others are visibly curious.

ERIC stands up, eyes locked with KYLE.

**ERIC**
It's about flexibility, Kyle. You're too rigid!

KYLE stands as well, matching Eric's stance.

**KYLE**
And you're too loose with your principles!

The BARTENDER (50s, with a thick beard and a worn "Peacekeeper" apron) notices the tension rising and steps over.

**BARTENDER**
Hey, fellas, calm down. Code wars aren't worth a scene.

ERIC and KYLE exchange looks, a tense silence lingers before they reluctantly sit back down.

**ERIC**
(sighing)
Maybe... we could agree to disagree?

**KYLE**
(grumbling)
Fine. But four spaces are objectively better.

ERIC chuckles, taking a swig of his beer.

**ERIC**
We'll see about that.

The tension eases as they return to their laptops, their argument a new chapter in their ongoing friendship."""

class TestExtractScreenplayTest(unittest.TestCase):

    def test_extraction(self):
        actual_text = extract_screenplay_text(input_text)
        self.assertEqual(actual_text, expected_text)

    def test_no_extraction(self):
        no_screenplay_text = "This is not a screenplay."
        actual_text = extract_screenplay_text(no_screenplay_text)
        self.assertEqual(actual_text, "")

if __name__ == '__main__':
    unittest.main()
