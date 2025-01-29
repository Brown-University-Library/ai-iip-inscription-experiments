from leidenmark_local.leidenmark.__init__ import leiden_plus, leiden_escape


content = """\
<D=.r<=
Εἶς θε[ὸ]ς μόνος βο[ήθει] Κασσ<ι>[α]νῷ ἅμα συμβίῳ καὶ τέ[κ]νοις καὶ πάσει.
=>=D>"""

content = """\
<D=.r<=
1. ((+)) ὑπὲρ σωτη
2.-ρίας προσφο
3.-ράς Ματρώνας
=>=D>"""

content = """\
<D=.r<=
Εἶς θεὸ[ς μόνο-]
ς ὁ βοηθ[ῶν] 
Γαδιωναν 
κ(αὶ) Ἰουλιανῷ 
κ(αὶ) πᾶσιν τοῖς ἀξί-
οις 
=>=D>"""


print(leiden_plus(content, indent=True))