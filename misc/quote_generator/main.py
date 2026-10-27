import random

quotes = [
    ("It is only with the heart that one can see rightly; what is essential is invisible to the eye.", "Antoine de Saint Exupéry"),
    ("There comes a time when we must choose between what is right and what is easy.", "Albus Dumbledore"),
    ("It is our choices, Harry, that show what we truly are, far more than our abilities.", "Albus Dumbledore"),
    ("Courage is not the absence of fear; rather it is the recognition that something else is more important than fear.", "The Princess Diaries"),
    ("We are not human beings having a spiritual experience; we are spiritual beings having a human experience.", "Pierre Teilhard de Chardin"),
    ("If you have built castles in the air, your work need not be lost; that is where they should be. Now put foundations under them.", "Henry David Thoreau"),
    ("What comes into our minds when we think about God is the most important thing about us.", "A.W. Tozer"),
    ("Life can only be understood backward, but it must be lived forward.", "Kierkegaard"),
    ("We can never see past the choices we don't understand.", "The Matrix"),
    ("The best way to predict the future is to create it.", "Abraham Lincoln")
]

selection = random.choice(quotes)

print(f"'{selection[0]}' -- {selection[1]}")