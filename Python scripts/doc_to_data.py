from bs4 import BeautifulSoup
import mammoth


# Custom CSS for styling of cards
custom_css = """
    <style>
    .underlinebold{
        text-decoration: underline;
        font-weight: bold;
    }
    .emphasis{
       text-decoration: underline;
       font-weight: bold;
       #border-width:1px;
       #border-style:solid;
       
    }
    .highlighted{
        background-color: #5DE23C;
    }
    .font7{
        font-size: 0.63em;
    }
    .font6{
        font-size: 0.54em;
    }

    
    </style>
"""

# Styling map for DOCX
style_map ="""
    u => u
    b => strong
    i => em
    highlight => r.highlighted

    r.underline => u
    r.Style13ptBold => strong
    r.StyleUnderline => u
    r.UnderlineBold => r.underlinebold
    r.Emphasis => r.emphasis
    r.textbold => r.emphasis
    
    
"""


def card_to_data(file_path):
    # Open file and convert using style mapping
    with open(file_path, "rb") as file:
        output = mammoth.convert_to_html(file, style_map = style_map)
        print(output.messages)
        output = output.value
        
    # Write converted into a file for debuging
    with open("conversion.html", "w", encoding="utf8") as file:
        file.write(custom_css + output)

    
    # Open Beautiful Soup
    soup = BeautifulSoup(output, "lxml")

    # Find Cards
    cards = soup.find_all('h4')
    

    # Loop Through Card Data
    data = []
    for tag in cards:
        try:
            
            # Extract Card Data
            citation = tag.find_next("p")
            card = tag.find_next("p").find_next("p")

            # Number of Words in Doc
            doc_word_length = len(card.text.split())
            
            if doc_word_length >= 70:
                data.append({"tag" : str(tag),
                            "cite" : str(citation),
                            "cardHTML" : str(tag) + str(citation) + str(card),
                            })
            else:
                print("Skipped because Malformed: " + str(tag))
            
        except AttributeError as e:
            print("Error: " + str(e))
            pass      
    return data

def test_code():
    data = card_to_data("test_doc.docx")
    card_counter = 0
    with open("output.html", "w", encoding = "utf-8") as test:
        test.write(custom_css)
        for card in data:
            card_counter += 1
            test.write("<br> <br> Card Number: " + str(card_counter) + "<br> <br>" + card["cardHTML"])

test_code()
