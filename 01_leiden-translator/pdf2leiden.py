import os
from dotenv import load_dotenv
import anthropic
import base64

def extract_leiden(pdf) -> str:

    client = anthropic.Anthropic(
        # defaults to os.environ.get("ANTHROPIC_API_KEY")
        api_key=os.environ.get("ANTHROPIC_API_KEY")
    )

    # If necessary, I can also talk about how a PDF can encode Leiden symbols in a non-textual manner
    # and also provide more details on the Leiden notations.
    instruction = '''You are an expert system designed to extract epigraphic and papyrological inscriptions transcribed according to the Leiden Convention (from now called Leiden transcripts) from a PDF.
    Your task is to output a string that contain accurate copies of all Leiden transcripts present in the PDF, including accurate representation of all characters (including Greek, Hebrew, and Aramaic characters) and Leiden symbols (such as '[', '(', and '-').
    '''

    pdf_data = base64.standard_b64encode(pdf).decode("utf-8")
    # print(base64.standard_b64decode(pdf_data))

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
                        "text": "Below are example parts of processed PDF inputs and the corresponding outputs containing Leiden transcriptions."
                                + "<examples>\n" 
                                + "<example>\n<Input>\nThis inscription was found on a mosaic floor pattern in East Jerusalem. ΕΙΣ ΘΕΟ\nΣΟΒΟΗΘ\nΓΑΔΙΩΝΑΝ\nΚΙΟΥΛΙΑΝΩ\nΚΠΑΣΙΝΤΟΙΣΑΞ\nΙΟΙΣ\nפעלהבדה\n\nΕἶς θεὸ[ς μόνο-] \nς ὁ βοηθ[ῶν] \nΓαδιωναν \nκ(αὶ) Ἰουλιανῷ \nκ(αὶ) πᾶσιν τοῖς ἀξί- \nοις \nפעלהבדה\n\nAnd here is the translation.\nOnly one god who helps Gadiona and Iulianus and all who deserve it. (Made it from his) possession in this place.\n\nThis mosaic flooring was found with many other objects such as the urn and the vase shown in the next page. The style of the mosaic tiling resembles that of the early 3rd century Christian inscriptions.</Input>\n<Ideal_Output>\n     <inscription>\n       Εἶς θεὸ[ς μόνο-] \n     ς ὁ βοηθ[ῶν] \n     Γαδιωναν \n     κ(αὶ) Ἰουλιανῷ \n       κ(αὶ) πᾶσιν τοῖς ἀξί- \n        οις \       nפעלהבדה\n  </inscription>\n</Ideal_Outp<ut>\n</example>\n"
                                + "<example>\n<Input>\nNext, on the altar to the east of the chapel, you can find a devotionary inscription.\n\nΚΕΜΝΗΣΤΩΝΠΡ\nΝΕΚΑΝΤΚΑΙ\n\nΚ(ύρι)ε μνήσ(θητι) τῶν πρ-\n[οσ]νε(γ)καντ(ων) καὶ\n[---]\n\nHere is the translation.\nLord, remember the first song...\n\nThis inscription is very similar in its form to another inscription from a nearby altar which is shown below.</Input>\n<Ideal_Output>\n     <inscription>\n     Κ(ύρι)ε μνήσ(θητι) τῶν πρ-\n        [οσ]νε(γ)καντ(ων) καὶ\n     [---]\n    </inscription>\n</Ideal_Output>\n</example>\n"
                                + "</examples>\n\n"
                    },
                    {
                        "type": "text",
                        "text": "Following is the PDF file from which you should extract Leiden transcriptions.\n"
                    },
                    {
                        "type": "document",
                        "source": {
                            "type": "base64",
                            "media_type": "application/pdf",
                            "data": pdf_data
                        }
                    }
                ]
            }
        ]
    )
    
    return message.content[0].text

def extract_diplomatic_leiden_translation(pdf) -> str:

    client = anthropic.Anthropic(
        # defaults to os.environ.get("ANTHROPIC_API_KEY")
        api_key=os.environ.get("ANTHROPIC_API_KEY")
    )

    # If necessary, I can also talk about how a PDF can encode Leiden symbols in a non-textual manner
    # and also provide more details on the Leiden notations.
    instruction = '''You are an expert system designed to extract epigraphic and papyrological inscriptions from a PDF.
    Your task is to output a string that contain accurate copies of all Diplomatic transcripts and Leiden transcripts of the inscriptions present in the PDF, along with its translation, if present.
    Including accurate representation of all characters (including Greek, Hebrew, and Aramaic characters) and Leiden symbols (such as '[', '(', and '-').
    '''

    pdf_data = base64.standard_b64encode(pdf).decode("utf-8")
    # print(base64.standard_b64decode(pdf_data))

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
                        "text": "Below are example parts of processed PDF inputs and the corresponding outputs containing Leiden transcriptions."
                                + "<examples>\n" 
                                + "<example>\n<Input>\nThis inscription was found on a mosaic floor pattern in East Jerusalem.\n\nΕΙΣ ΘΕΟ\nΣΟΒΟΗΘ\nΓΑΔΙΩΝΑΝ\nΚΙΟΥΛΙΑΝΩ\nΚΠΑΣΙΝΤΟΙΣΑΞ\nΙΟΙΣ\nפעלהבדה\n\nΕἶς θεὸ[ς μόνο-] \nς ὁ βοηθ[ῶν] \nΓαδιωναν \nκ(αὶ) Ἰουλιανῷ \nκ(αὶ) πᾶσιν τοῖς ἀξί- \nοις \nפעלהבדה\n\nAnd here is the translation.\nOnly one god who helps Gadiona and Iulianus and all who deserve it. (Made it from his) possession in this place.\n\nThis mosaic flooring was found with many other objects such as the urn and the vase shown in the next page. The style of the mosaic tiling resembles that of the early 3rd century Christian inscriptions.</Input>\n<Ideal_Output>\n<diplomatic>ΕΙΣ ΘΕΟ\nΣΟΒΟΗΘ\nΓΑΔΙΩΝΑΝ\nΚΙΟΥΛΙΑΝΩ\nΚΠΑΣΙΝΤΟΙΣΑΞ\nΙΟΙΣ\nפעלהבדה\n</diplomatic>\n<leiden>\nΕἶς θεὸ[ς μόνο-] \nς ὁ βοηθ[ῶν] \nΓαδιωναν \nκ(αὶ) Ἰουλιανῷ \nκ(αὶ) πᾶσιν τοῖς ἀξί- \nοις \       nפעלהבדה\n</leiden>\n<translation>Only one god who helps Gadiona and Iulianus and all who deserve it. (Made it from his) possession in this place.</translation>\n</Ideal_Outp<ut>\n</example>\n"
                                + "<example>\n<Input>\nNext, on the altar to the east of the chapel, you can find a devotionary inscription.\n\nΚΕΜΝΗΣΤΩΝΠΡ\nΝΕΚΑΝΤΚΑΙ\n\nΚ(ύρι)ε μνήσ(θητι) τῶν πρ-\n[οσ]νε(γ)καντ(ων) καὶ\n[---]\n\nThis inscription is very similar in its form to another inscription from a nearby altar which is shown below.</Input>\n<Ideal_Output>\n<diplomatic>ΚΕΜΝΗΣΤΩΝΠΡ\nΝΕΚΑΝΤΚΑΙ\n</diplomatic>\n<leiden>\nΚ(ύρι)ε μνήσ(θητι) τῶν πρ-\n[οσ]νε(γ)καντ(ων) καὶ\n[---]\n</leiden>\n<translation></translation>\n</Ideal_Output>\n</example>\n"
                                + "</examples>\n\n"
                    },
                    {
                        "type": "text",
                        "text": "Following is the PDF file from which you should extract Diplomatic transcriptions, Leiden transcriptions, and their translations.\n"
                    },
                    {
                        "type": "document",
                        "source": {
                            "type": "base64",
                            "media_type": "application/pdf",
                            "data": pdf_data
                        }
                    }
                ]
            }
        ]
    )
    
    return message.content[0].text

if __name__=="__main__":
    load_dotenv()
    flag = 0

    path = "01_leiden-translator/"
    pdf_files = [x for x in os.listdir(path + 'data/inscription_PDFs') if x[-4:] == '.pdf']
    leiden_txt_files = [x for x in os.listdir(path + 'leiden_from_pdf') if x[-4:] == '.txt']
    for tf in pdf_files:
        if tf == "(IEP,short)Goldwasser-EarlyAlphabeticInscriptions-2022.pdf":
            continue
        if tf == "(IEP,table)Lieberman-ItsAnotherBrick-2022.pdf":
            continue
        if tf[:-4] + ".txt" in leiden_txt_files:
            continue
        # if flag == 1:
        #     continue
        # if flag == 0:
        #     flag = 1
        
        print("opened " + tf)
        rf = open("01_leiden-translator/data/inscription_PDFs/" + tf, "rb")
        pdf = rf.read()
        leiden = extract_leiden(pdf)
        diplomatic_leiden_translation = extract_diplomatic_leiden_translation(pdf)
        rf.close()
        print("read " + tf)

        wf = open("01_leiden-translator/leiden_from_pdf/" + tf[:-4] + ".txt", "a")
        wf.write(leiden)
        wf.close()

        wf = open("01_leiden-translator/dplm_ldn_trns_from_pdf/" + tf[:-4] + ".txt", "a")
        wf.write(diplomatic_leiden_translation)
        wf.close()