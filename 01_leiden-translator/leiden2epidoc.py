import os
import anthropic

def get_epidoc(leiden) -> str:

    client = anthropic.Anthropic(
        # defaults to os.environ.get("ANTHROPIC_API_KEY")
        api_key="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",
    )

    instruction = '''You are an expert system designed to translate epigraphic and papyrological inscriptions from Leiden Conventions format into XML that conforms to the EpiDoc schema. 
Your task is to accurately convert the given text, preserving all meaningful information while translating the special symbols into appropriate XML tags. 
When translating the text, please make sure to meticulously follow the guideline below tagged <instruction> for translating specific Leiden Convention symbols to EpiDoc-compliant XML. 
                
<instruction>
Note: you may encounter variations on these Leiden conventions that look slightly different, but
the following is a general guide to how you would represent what you see in an edited
inscription in EpiDoc XML.

IMPORTANT: Make sure that all attribute tags are limited to a single word with no white-
space in between. Thus, rather than encoding something as
<supplied reason=”lost”>Marcus Verus</supplied>,
you MUST encode it as
<supplied reason=”lost”>Marcus</supplied> <supplied
reason=”lost”>Verus</supplied>.
The reason for this is that the wordlist identifies spaces as word breaks, so we do not want
any attributes where there is a space. There are a few exceptions where spaces within tags
are okay (i.e., <foreign> tags, <choice> tags involving multiple words within a given
option).

Abbreviations
- Description: expansion of words abbreviated in the inscription
- Sample Leiden Input: v(iro)
- Corresponding EpiDoc Output: <expan><abbr>v</abbr><ex>iro</ex></expan>

Abbreviation Marks
- Description: At times, an abbreviation is signaled through an additional letter or a punctuation mark. Any characters or symbols that appear in the abbreviated form on the support (<abbr>), but do not form part of the fully expended word (<expan>), should be included within the <abbr> element, and should additionally be enclosed in an <am> (abbreviation mark) element.
- Sample Leiden Input: Augg(usti)
- Corresponding EpiDoc Output: <expan><abbr>Aug<am>g</am></abbr><ex>usti duo</ex></expan>

Alternative Readings
- Description: Alternate readings posited by the editor. Preferred reading (<lem>) will appear in the text, the alternative (<rdg>) in the apparatus.
- Sample Leiden Input: Ὀχυρυγχίτου|alt|Ὀξυρυγχίτου νομοῦ
- Corresponding EpiDoc Output: <app type="alternative"><lem>Ὀχυρυγχίτου</lem><rdg>Ὀξυρυγχίτου νομοῦ</rdg></app>

Ambiguous characters with alternatives offered
- Description: Use the following tagging. This is often indicated either in a critical apparatus, with a slash, a question mark, or the word “or”.
- Sample Leiden Input 1: α/β
- Corresponding EpiDoc Output 1: <choice><unclear>α</unclear><unclear>β</unclear></choice>
- Sample Leiden Input 2: α or β
- Corresponding EpiDoc Output 2: <choice><unclear>α</unclear><unclear>β</unclear></choice>
- Sample Leiden Input 3: α? or β?
- Corresponding EpiDoc Output 3: <choice><unclear>α</unclear><unclear>β</unclear></choice>

Bilingual Inscriptions
- Description: When two languages (e.g. Greek and Hebrew) appears on the same support and within one and the same text, the language that appears second is marked as <foreign> in the edited transcription, with the indication of the relevant language in the xml:lang attribute.
- Sample Leiden Input: δοῦλος θεοῦ אבג
- Corresponding EpiDoc Output: δοῦλος θεοῦ <foreign xml:lang=“heb”>אבג</foreign>

Deletion
- Description: If an object preserves traces of an inscription that has been rubbed out, or otherwise removed, editors represent the text in double square brackets. In our corpus, if it is still somehow legible, erased text is represented as follows both in the diplomatic and in the edited transcription boxes:
- Sample Leiden Input: [[Legio]]
- Corresponding EpiDoc Output: <del rend=“erasure”>Legio</del>

Deleted and Illegible
- Description: letters erased from the original inscription and no longer legible
- Sample Leiden Input: [[...]]
- Corresponding EpiDoc Output: <del rend=“erasure"><gap reason="lost" quantity="3" unit="character"/></del>

Illegible characters
- Description: traces of letters visible on the stone, but it is impossible to recognize what they are; one cross stands for each letter.
- Sample Leiden Input: + + +
- Corresponding EpiDoc Output: <gap reason="illegible" quantity="3" unit="character"/>

Lost Letters of a Precise Length
- Description: letters lost that cannot be restored, the precise number of which can be conjectured (one full-stop for each lost letter)
- Sample Leiden Input: [.....]
- Corresponding EpiDoc Output: <gap reason="lost" quantity="5" unit="character"/>

Lost Letters of Approximate Length
- Description: letters lost that cannot be restored, the approximate number of which can be conjectured
- Sample Leiden Input: [-c.6-]
- Corresponding EpiDoc Output: <gap reason="lost" atLeast="4" atMost="6" unit="character"/>

Lost Letters with a Range of Length
- Description: letters lost that cannot be restored, with a range of the number of them
- Sample Leiden Input: [-5-6-]
- Corresponding EpiDoc Output: <gap reason=“xyz” atLeast=“5” atMost= “6” unit=&quot;character&quot;/>

Lost Letters with a Physical Size
- Description: letters lost that cannot be restored, occupying a physical space of a certain size
- Sample Leiden Input: [-5 cm-]
- Corresponding EpiDoc Output: <gap reason=“xyz” extent=&quot;5&quot; unit=&quot;cm&quot;/>

Lost Letters of Unknown Length
- Description: letters lost that cannot be restored and their precise number cannot be conjectured
- Sample Leiden Input: [- - -]
- Corresponding EpiDoc Output: <gap reason="lost" extent="unknown" unit="character"/>

Lost Line
- Description: loss of complete line
- Sample Leiden Input: [- - - - - -]
- Corresponding EpiDoc Output: <gap reason="lost" quantity="1" unit="line"/>

Lost Lines
- Description: Loss of multiple lines
- Sample Leiden Input: - - - - - -
- Corresponding EpiDoc Output: <gap reason="lost" extent="unknown" unit="line"/>

Ligature
- Description: two or more letters are joined together to form a single sign
- Sample Leiden Input: ȣ
- Corresponding EpiDoc Output: <hi rend=&quot;ligature&quot;>ου</hi>

Line break
- Description: Mark a line break at the beginning of every line, except the final one. If the inscription is only one line long, do not enter a line break tag. Note that a <lb/> tag can occur in the middle of the word. When this is the case, it is important NOT to put any spaces between the tag and the continuation of the word if you are working in Text Mode and not to actually type a hyphen.
- Sample Leiden Input: Ave
Legio Fre-
tensis
- Corresponding EpiDoc Output: <lb/>Ave <lb/>legio Fre<lb break=”no”/>tensis

Symbols
- Description: the editor's explanation of letters or symbols; e.g., inverted or retrograde letters, numerals ((decem milia)) or symbols ((centuria)), ((mulieris))
- Sample Leiden Input 1: ((+))
- Corresponding EpiDoc Output 1: <g ref=“cross”>+</g>
- Sample Leiden Input 2: ((centuria))
- Corresponding EpiDoc Output 2: <g ref="centuria"/>

Numbers
- Description: A number or a fraction should always be placed inside a <num> tag, with the indication of their value.
- Sample Leiden Input: ἑλαία φολὲ Δ Δ γεῖτ
- Corresponding EpiDoc Output: ἑλαία φολὲ <num value="20">Δ Δ</num> γεῖτ

Numbers with Supraline or Underline
- Description: At times, a line above or below the letters indicates that they have a numeric value. If this happens, it is tagged as follows (both in diplomatic and in edited transcription):
- Corresponding EpiDoc Output: <num value=“5”><hi rend=“supraline”>ε</hi></num>

Greek Numerals with Marks
- Description: Greek numerals are Greek letters marked with a tick (ʹ) (Unicode character code: 0374) at the upper right, which looks like an apostrophe. So, in Greek transcriptions look carefully for the difference between number signs and the very rare apostrophe. There is also an occasional number mark at the lower left of a Greek numeral, like a comma (͵) (Unicode character code: 0375).
- Sample Leiden Input: δεκάτῃ ἰνδ(ικτιῶνος) ιδʹ ἡμέρᾳ
- Corresponding EpiDoc Output: <lb/>δεκάτῃ <expan><abbr>ἰνδ</abbr><ex>ικτιῶνος</ex></expan> <num value="14">ιδʹ</num> ἡμέρᾳ

Regularization
- Description: This tagging is used to indicate text normalized or regularized by the editor from a dialect or phonetic spelling, grammatical form, etc., usually for whole words (as opposed to sic/corr, which typically is used for single characters: see below). This is always nested within <choice></choice>.
- Sample Leiden Input: πρεσβύτερος (an unusual spelling of πρεσβίτιρος)
- Corresponding EpiDoc Output: <choice><reg>πρεσβύτερος</reg><orig>πρεσβίτιρος</orig></choice>

Phoenician (paleo-Hebrew) letters and/or numerals
- Description: (cf. e.g. ostraca from Masada) We use a glyph tagging in these cases. Each letter needs to be tagged separately as a glyph, and identified using the Unicode name as shown in the link below.
- Corresponding EpiDoc Output 1: <g ref=&quot;phoen_three&quot;/>
- Corresponding EpiDoc Output 2: <g ref=“phoen_alef”/>

Raised/Lowered characters
- Description: Within the same word, some characters may at times appear above or below the rest.
- Corresponding EpiDoc Output: E=mc<hi rend=“superscript”>2</hi>

Superfluous Text
- Description: Erroneously included text is usually indicated with '{' and '}' in the printed edition.
- Sample Leiden Input: {xyz}
- Corresponding EpiDoc Output: <surplus>xyz</surplus>

Supplied Lost Text
- Description: Letters are usually missing because the text area is damaged, or because the writer of the inscription made a mistake.
- Sample Leiden Input: Le[g]
- Corresponding EpiDoc Output: Le<supplied reason=“lost”>g</supplied>

Uncertain Supplied Lost Text
- Description: restoration of letters that are now lost, but restoration is not definite
- Sample Leiden Input: [abc ?]
- Corresponding EpiDoc Output: <supplied reason="lost" cert="low">abc</supplied>

Supplied Omitted Text
- Description: Angle brackets typographically indicate letters omitted by the writer of the inscription and supplied by the editor.
- Sample Leiden Input: L<e>g
- Corresponding EpiDoc Output: L<supplied reason=“omitted”>e</supplied>g

Spelling Mistake
- Description: This is used to indicate words that the writer misspelled. Editors often typographically mark this
with (!).
- Sample Leiden Input: Augostus
- Corresponding EpiDoc Output: <choice><corr>Augustus</corr><sic>Augostus</sic></choice>

Unclear Letters
- Description: A standard way to indicate an unclear character when publishing inscriptions is to have the letters appear with a dot below it.
- Sample Leiden Input 1: Laviniạ
- Corresponding EpiDoc Output 1: Lavini<unclear>a</unclear>
- Sample Leiden Input 2: Lavinia?
- Corresponding EpiDoc Output 2: Lavini<unclear>a</unclear>

Vacat
- Description: Spaces left intentionally blank by the writer of the inscription.
- Sample Leiden Input: (vac.)
- Corresponding EpiDoc Output: <space extent=“unknown” unit=“character”/>
<instruction>

Before providing your final translation, first wrap the following steps in tags and include them in your response: 
1. Read through the entire text to familiarize yourself with its content and structure.
2. List all Leiden Convention symbols present in the given text.
3. Map each identified symbol to its corresponding EpiDoc XML tag using the guideline above tagged <instruction>.
4. Consider and explain how you will handle nested tags and their proper order.
5. Outline any potential challenges in the translation and how you plan to address them.

Second, check the following before providing your final translation: 
1. Preserve all alphabetic characters and spaces as they appear in the original text. 
2. Review your translation to ensure all symbols have been accurately converted and tags are properly nested. 

This detailed breakdown will help ensure a thorough and accurate translation. After your analysis, provide the final XML translation wrapped in tags. Ensure that your output strictly adheres to the EpiDoc schema and conventions.'''

    # Replace placeholders like {{Input}} with real values,
    # because the SDK does not support variables.
    message = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=8192,
        temperature=0,
        system=instruction,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "Below are example inputs written according to the Leiden convention and the corresponding outputs in XML following the EpiDoc convention."
                                + "<examples>\n" 
                                + "<example>\n<Input>\nΕἶς θεὸ[ς μόνο-] \nς ὁ βοηθ[ῶν] \nΓαδιωναν \nκ(αὶ) Ἰουλιανῷ \nκ(αὶ) πᾶσιν τοῖς ἀξί- \nοις \n</Input>\n<ideal_output>\n<div type=\"edition\" subtype=\"transcription\" ana=\"b1\">\n                <p>\n                    <lb/>Εἶς θεὸ<supplied reason=\"lost\">ς</supplied> <supplied reason=\"lost\">μόνο</supplied><lb break=\"no\"/>ς ὁ\n                        βοηθ<supplied reason=\"lost\">ῶν</supplied>\n                    <lb/>Γαδιωναν <lb/><expan><abbr>κ</abbr><ex>αὶ</ex></expan> Ἰουλιανῷ\n                            <lb/><expan><abbr>κ</abbr><ex>αὶ</ex></expan> πᾶσιν τοῖς ἀξ<lb break=\"no\"/>ίοις <lb/><foreign xml:lang=\"heb\">פעלהבדה</foreign></p>\n            </div>\n</ideal_output>\n</example>\n"
                                + "<example>\n<Input>\nΚ(ύρι)ε μνήσ(θητι) τῶν πρ-\n[οσ]νε(γ)καντ(ων) καὶ\n[---] \n</Input>\n<ideal_output>\n<div type=\"edition\" subtype=\"transcription\" ana=\"b1\">\n                <p>\n                    <lb/><expan><abbr>Κ</abbr><ex>ύρι</ex><abbr>ε</abbr></expan> <expan><abbr>μνήσ</abbr><ex>θητι</ex></expan> τῶν <expan><abbr>πρ<lb break=\"no\"/><supplied reason=\"lost\">οσ</supplied>νε</abbr><ex>γ</ex><abbr>καντ</abbr><ex>ων</ex></expan> καὶ <lb/><gap reason=\"lost\" extent=\"unknown\" unit=\"character\"/></p>\n            </div>\n</ideal_output>\n</example>\n"
                                + "<example>\n<Input>\nεἷς θεὸς ὁ νικῶν τὰ κα[κὰ] \nἸάω θ[εὸς] \nεἷς θ[εὸ]ς \n</Input>\n<ideal_output>\n<div type=\"edition\" subtype=\"transcription\" ana=\"b1\">\n                <p>\n                    <lb/>εἷς θεὸς ὁ νικῶν τὰ κα<supplied reason=\"lost\">κὰ</supplied> <lb/> Ἰάω θ<supplied reason=\"lost\">εὸς</supplied> <lb/>εἷς θ<supplied reason=\"lost\">εὸ</supplied>ς </p>\n            </div>\n</ideal_output>\n</example>\n"
                                + "<example>\n<Input>\nΚ(ύρι)ε Ἰ(ησο)ῦ Χ(ριστ)ὲ πρόσδεξε τὴν \nκαρποφορίαν τῶν δούλω(ν) \nσοῦ Ἰωάννου τοῦ πρ(εσβυτέρ)ου καὶ \nἈββοσόβου ὅτι ἐξ ἰδίων κό-\nπων ἤγιραν τὸν οἴκον τοῦτον.\n</Input>\n<ideal_output>\n<div type=\"edition\" subtype=\"transcription\" ana=\"b1\">\n                <p>\n                    <lb/><expan><abbr>Κ</abbr><ex>ύρι</ex><abbr>ε</abbr></expan> <expan><abbr>Ἰ</abbr><ex>ησο</ex><abbr>ῦ</abbr></expan> <expan><abbr>Χ</abbr><ex>ριστ</ex><abbr>ὲ</abbr></expan> πρόσδεξε τὴν <lb/>καρποφορίαν τῶν <expan><abbr>δούλω</abbr><ex>ν</ex></expan> <lb/>σοῦ Ἰωάννου τοῦ <expan><abbr>πρ</abbr><ex>εσβυτέρ</ex><abbr>ου</abbr></expan> καὶ <lb/>Ἀββοσόβου ὅτι ἐξ ἰδίων κό<lb break=\"no\"/>πων ἤγιραν τὸν οἴκον τοῦτον.</p>\n            </div>\n</ideal_output>\n</example>\n"
                                + "<example>\n<Input>\nἘπὶ τοῦ <δ>ὁσιωτάτου Γεωργίου δια-\nκόνου καὶ Ϲαμουήλου λαμπροτ(άτου)\nκαὶ Ἀββεος Ζαχαρίου ἐγένετο τὸ π(ᾶν)\nἔργον τ<ῆ?>ς ψιφώσεως ταύτης\nἐν μ(ηνὶ) Ἱουν[ίῳ ἔτους] [Ἐλευθερο]πόλε(ως) βφʹ\n</Input>\n<ideal_output>\n<div type=\"edition\" subtype=\"transcription\" ana=\"b1\">\n                <p>\n                    <lb/>Ἐπὶ τοῦ <supplied reason=\"omitted\">δ</supplied>ὁσιωτάτου Γεωργίου δια<lb break=\"no\"/>κόνου καὶ Ϲαμουήλου <expan><abbr>λαμπροτ</abbr><ex>άτου</ex></expan><lb/>καὶ Ἀββεος Ζαχαρίου ἐγένετο τὸ <expan><abbr>π</abbr><ex>ᾶν</ex></expan><lb/>ἔργον τ<supplied reason=\"omitted\" cert=\"low\">ῆ</supplied>ς ψιφώσεως ταύτης<lb/>ἐν <expan><abbr>μ</abbr><ex>ηνὶ</ex></expan> Ἱουν<supplied reason=\"lost\">ίῳ</supplied> <supplied reason=\"lost\">ἔτους</supplied> <supplied reason=\"lost\"><abbr><expan>Ἐλευθερο</expan></abbr></supplied><expan><abbr>πόλε</abbr><ex>ως</ex></expan> <num value=\"502\">βφʹ</num></p>\n            </div>\n</ideal_output>\n</example>\n"
                                + "<example>\n<Input>\n[Ἐπὶ Σι]λουανοῦ θεοφιλ(εστάτου) διακό(νου) κ(αὶ) ἡγουμέ(νου) ἡ παροῦσα\n[ψήφωσ]ις ἐγένετο κ(αὶ) κόγχη κ(αὶ) ἡ προσθήκη τοῦ ναοῦ μ<ή>κος \n[πήχεις ... ὕ]ψους π(ή)χ(εις) ς' μνήσθητ[ί μου] Κ(ύρι)ε ἐν [τῇ β]ασιλ<ε>ίᾳ σου.\n</Input>\n<ideal_output>\n<div type=\"edition\" subtype=\"transcription\" ana=\"b1\">\n                <p>\n                    <lb/><supplied reason=\"lost\">Ἐπὶ</supplied> <supplied reason=\"lost\">Σι</supplied>λουανοῦ <expan><abbr>θεοφιλ</abbr><ex>εστάτου</ex></expan> <expan><abbr>διακό</abbr><ex>νου</ex></expan> <expan><abbr>κ</abbr><ex>αὶ</ex></expan> <expan><abbr>ἡγουμέ</abbr><ex>νου</ex></expan> ἡ παροῦσα <lb/><supplied reason=\"lost\">ψήφωσ</supplied>ις ἐγένετο <expan><abbr>κ</abbr><ex>αὶ</ex></expan> κόγχη <expan><abbr>κ</abbr><ex>αὶ</ex></expan> ἡ προσθήκη τοῦ ναοῦ μ<supplied reason=\"omitted\">ή</supplied>κος <lb/><supplied reason=\"lost\">πήχεις</supplied> <gap reason=\"lost\" extent=\"unknown\" unit=\"character\"/> <supplied reason=\"lost\">ὕ</supplied>ψους <expan><abbr>π</abbr><ex>ή</ex><abbr>χ</abbr><ex>εις</ex></expan> <num value=\"6\">ς'</num> μνήσθητ<supplied reason=\"lost\">ί</supplied> <supplied reason=\"lost\">μου</supplied> <expan><abbr>Κ</abbr><ex>ύρι</ex><abbr>ε</abbr></expan> ἐν <supplied reason=\"lost\">τῇ</supplied> <supplied reason=\"lost\">β</supplied>ασιλ<supplied reason=\"omitted\">ε</supplied>ίᾳ σου.</p>\n            </div>\n</ideal_output>\n</example>\n"
                                + "<example>\n<Input>\n(+) Ἀνεπάη μακά-\nριος Ζαχαρίας \nἘρασίνου ἐν \nμηνὶ Πανέμου \nδεκάτῃ ἰνδ(ικτιῶνος) ιδʹ ἡ-\nμέρᾳ κυριακῇ ὧραν \nτρίτῃ τῆς νυκτὸς κα-\nτετέθη δὲ ἐνταῦθα \nτῇ τρίτῃ τοῦ σάμ-\nβατος ὥραν ὀγδόην \nΠανέμῷ δοδεκα-\nτῃ ἰν(δικτιῶνος) ιδʹ ἔτους κα-\nτὰ Ἐλού(σην) ΥΟςʹ Κ(ύρι)ε ἀ-\nνάπαυσον τὴν ψυ-\nχὴν αὐτοῦ μετὰ τῶν \nἁγίων σου. Ἀμήν\n</Input>\n<ideal_output>\n<div type=\"edition\" subtype=\"transcription\" ana=\"b1\">\n                <p>\n                    <lb/><g ref=\"cross\">+</g> Ἀνεπάη μακά<lb break=\"no\"/>ριος Ζαχαρίας\n                    <lb/>Ἐρασίνου ἐν\n                    <lb/>μηνὶ Πανέμου\n                    <lb/>δεκάτῃ <expan><abbr>ἰνδ</abbr><ex>ικτιῶνος</ex></expan> <num value=\"14\">ιδʹ</num> ἡ<lb break=\"no\"/>μέρᾳ κυριακῇ ὧραν\n                    <lb/>τρίτῃ τῆς νυκτὸς κα<lb break=\"no\"/>τετέθη δὲ ἐνταῦθα\n                    <lb/>τῇ τρίτῃ τοῦ σάμβα<lb break=\"no\"/>τος ὥραν ὀγδόην\n                    <lb/>Πανέμῷ δοδεκα<lb break=\"no\"/>τῃ <expan><abbr>ἰνδ</abbr><ex>ικτιῶνος</ex></expan> <num value=\"14\">ιδʹ</num> ἔτους κα<lb break=\"no\"/>τὰ <expan><abbr>Ἐλού</abbr><ex>σην</ex></expan> <num value=\"476\">ΥΟςʹ</num> <expan><abbr>Κ</abbr><ex>ύρι</ex><abbr>ε</abbr></expan> ἀ<lb break=\"no\"/>νάπαυσον τὴν ψυ<lb break=\"no\"/>χὴν αὐτοῦ μετὰ τῶν\n                    <lb/>ἁγίων σου. Ἀμήν</p>\n            </div>\n</ideal_output>\n</example>\n"
                                + "<example>\n<Input>\n[— ca. —]ς τεμένε. | [Ἐν Χαλκίδι] παρὰ τὸ τῆς Ἀθηναίας προσ[τόον (?)] | [. . . ἡμι]τέος ἢν γυὰι φορλὲς πλέθρα[—] | [. . .]ἐστὼ Δ Δ Δ Δ. vacat | [Ἐν Ἐστ]ιαίᾳ Ὀροβίδιοι Πανατ[—] | [. . .] ἑλαία φολὲ Δ Δ γεῖτ[ον. . .] | [. . .]γροι. vacat | [Ἐν Ἐρε]τρίαι Αἰγια[λέω . .!][—]\n</Input>\n<ideal_output>\n<div type=\"edition\" subtype=\"transcription\" ana=\"b1\">\n    <p>\n        <lb/><gap reason=\"lost\" extent=\"unknown\" unit=\"character\"/>ς τεμένε.\n        <lb/><supplied reason=\"lost\">Ἐν Χαλκίδι</supplied> παρὰ τὸ τῆς Ἀθηναίας προσ<supplied reason=\"lost\" cert=\"low\">τόον</supplied>\n        <lb/><gap reason=\"lost\" quantity=\"3\" unit=\"character\"/> <supplied reason=\"lost\">ἡμι</supplied>τέος ἢν γυὰι φορλὲς πλέθρα<gap reason=\"lost\" extent=\"unknown\" unit=\"character\"/>\n        <lb/><gap reason=\"lost\" quantity=\"3\" unit=\"character\"/>ἐστὼ <num value=\"40\">Δ Δ Δ Δ</num> <space/>\n        <lb/><supplied reason=\"lost\">Ἐν Ἐστ</supplied>ιαίᾳ Ὀροβίδιοι Πανατ<gap reason=\"lost\" extent=\"unknown\" unit=\"character\"/>\n        <lb/><gap reason=\"lost\" quantity=\"3\" unit=\"character\"/> ἑλαία φολὲ <num value=\"20\">Δ Δ</num> γεῖτ<gap reason=\"lost\" extent=\"unknown\" unit=\"character\"/>\n        <lb/><gap reason=\"lost\" quantity=\"3\" unit=\"character\"/>γροι <space/>\n        <lb/><supplied reason=\"lost\">Ἐν Ἐρε</supplied>τρίαι Αἰγια<supplied reason=\"lost\">λέω</supplied><gap reason=\"lost\" extent=\"unknown\" unit=\"character\"/>    </p>\n</div>\n</ideal_output>\n</example>\n"
                                + "<example>\n<Input>\nἘμ Π[οσειδῶν (?) ——] | Ἐμ Χα[λκίδ ——] | ἔλαιο[ν ——] | γεῖτο[ν ——]\n</Input>\n<ideal_output>\n<div type=\"edition\" subtype=\"transcription\" ana=\"b1\">\n    <p>\n        <lb/>Ἐμ Π<supplied reason=\"lost\" cert=\"low\">οσειδῶν</supplied> <gap reason=\"lost\" extent=\"unknown\" unit=\"character\"/>\n        <lb/>Ἐμ Χα<supplied reason=\"lost\">λκίδ</supplied> <gap reason=\"lost\" extent=\"unknown\" unit=\"character\"/>\n        <lb/>ἔλαιο<supplied reason=\"lost\">ν</supplied> <gap reason=\"lost\" extent=\"unknown\" unit=\"character\"/>\n        <lb/>γεῖτο<supplied reason=\"lost\">ν</supplied> <gap reason=\"lost\" extent=\"unknown\" unit=\"character\"/>\n    </p>\n</div>\n</ideal_output>\n</example>\n"
                                + "</examples>\n\n"
                    },
                    {
                        "type": "text",
                        "text": "Here is the text in Leiden Conventions format that you need to translate: \n\n<Input>\n" + leiden + "\n</Input>\n"
                    }
                ]
            }
        ]
    )
    
    return message.content[0].text

if __name__=="__main__":

    path = "01_leiden-translator/leiden"
    dir_list = [x for x in os.listdir(path) if x[-3:] == 'txt']
    for tf in dir_list:
        rf = open("01_leiden-translator/leiden/" + tf, "r")
        leiden = rf.read()
        epidoc = get_epidoc(leiden)
        rf.close()
        print("read " + tf)

        wf = open("01_leiden-translator/epidoc/" + tf, "a")
        wf.write(epidoc)
        wf.close()