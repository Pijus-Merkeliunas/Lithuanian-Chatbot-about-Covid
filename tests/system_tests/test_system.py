import threading
import unittest
from src.answer import look_for_answer
from src.database import connect_to_database


class SystemTest(unittest.TestCase):
    connect_to_database(testing=True)
#add to synonims saviizoliacija == izoliacija
    def test_program(self):
        # Arrange
        amount_succeded = 0
        testsmap = {

            'po kiek laiko prasideda koronos simptomai?':'Nuo dviejų dienų iki dviejų savaičių.',
            'ar rekia dėvėti kaukes autobusuose':'Pagal 2020-12-27 informacija, kaukes reikia dėvėti viešajame transporte',
            'kur prasidėjo korona?':'Kinijoje',
            'ar yra vaistas nuo koronos':'Taip, yra išrasta vakcina nuo koronos.',
            'ar yra vakcina nuo koronos':'Taip, yra išrasta vakcina nuo koronos.',
            'kaip plinta korona':'Koronavirusas yra perduodamas nuo žmogaus žmogui, dažniausiai artimo sąlyčio su sergančiuoju koronavirusine infekcija metu, pavyzdžiui, namų ar darbo aplinkoje, gydymo įstaigoje. COVID-19 taip pat gali būti perduodamas nuo žmogaus žmogui. Virusas plinta per orą kvėpavimo takų sekretų lašeliais, kuriuos žmonės išskiria į aplinką čiaudėdami, kosėdami ar iškvėpdami.',
            'kada bus vakcina nuo koronos?':'Vakcina jau yra išrasta.',
            'ar reikia dėvėti kaukes':'Pagal 2020-12-27 informacija, privaloma.',
            'kokie yra koronos simptomai?':'Simptomai yra panašūs į gripą – karščiavimas, kosulys, dusulys ir kiti kvėpavimo sutrikimai. Sunkesniais atvejais sukelia plaučių uždegimą, sepsį ir septinį šoką, inkstų nepakankamumą ar mirtį',
            'kaip išsygyditi nuo koronos?':'Specifinio gydymo nuo COVID-19 ligos nėra, taikomas tik simptominis gydymas. Susirgusieji gali būti visiškai išgydyti, priklausomai nuo jų sveikatos būklės bei nuo to, kada pradedamas taikyti gydyma',
            'kur skambinti dėl koronos?':'Karštoji linija Lietuvos gyventojams - 1808.',
            'ar galima keliauti po pasaulį?':'Pagal 2020-12-27 informacija, į kitas šalis galima keliauti, bet į kai kurias (kaip italija, kinija...) yra nerekomenduojama, taip pat kelionės į UK yra uždraustos.',
            'ar galiu išgyti nuo koronos?':'Taip, pasveikti yra įmanoma.',
            'ar galiu vaikšioti, lanyktis po miestą?':'Taip, bet patartina laikytis visų reikalavimų ir komendanto valandos.',
            'ar dabar yra karantinias':'Taip karantinas tesiasi iki 2020 metų sausio pabaigos.',
            'kiek laiko reikia izoliuotis?':'Saviizoliacija trunka 14 dienų.',
            'ar galima trumpiau saviizoliuotis':'Tiek Lietuvos piliečiai, tiek užsieniečiai turi galimybę sutrumpinti izoliacijos laiką, ne anksčiau kaip po 10 dienų atlikę koronaviruso testą. Gavus neigiamą rezultatą, izoliacijos laikas jiems gali būti sutrumpintas.',
            'ar veikia parkai, įvairūs renginiai':'Šiuo metu veiklos tokios kaip: sporto renginiai arba sporto klubai, pramogų parkai (pvz., baseinai,vandens parkai, batutų parkai) yra neveikiančios.',
            'ar verta čiaudėti į alkunę':'Lietuvos Respublikos sveikatos apsaugos ministerija skelbia, kad čiaudėjimas į alkunę yra veiksminga COVID-19 užsikrėtimų mažinimo priemonė.',
            'kas ta korona?':'COVID-19 yra virusas.',
            'ar dabar yra įvestas karantinas?': 'Šiuo metu šalyje yra paskelbtas karantinas.',
            'iki kelintos dirba parduotuvės?': 'Dirba tik maisto prekių parduotuvės, kurių darbo laikas šventiniu laikotarpiu gali būti kitoks.',
            'ar dėl koronos apribojamas transportas?': 'Palikti gyvenamąją vietą leidžiama: vykstant į darbą (darbo reikalais),prekybos vietą, į nuosavą nekilnojamojo turto objektą, laidotuves, dėl sveikatos priežiūros ir kitų būtinųjų paslaugų, pasivaikščioti atvirose vietose ne daugiau kaip vienos šeimos ar vieno namų ūkio nariams, vykstant prižiūrėti sergančių ar negalinčių savimi pasirūpinti asmenų.',
            'susirgau': 'Tokiu atveju turite skambinti į karštąją liniją numeriu - 1808.',
            'ar dezinfekcija apsaugo nuo koronos': 'Dezinfekcinio skysčio naudojimas sumažina riziką užsikrėsti korona.',
            'pyksti ant manęs?': 'Ne, nebent nesilaikai rekomendacijų.',
            'pyksti?': 'Ne, nebent nesilaikai rekomendacijų.',
            'ar užsikrėčiau?': 'Jei turite panašius simptomus kaip gripo t.y. karščiavimas, kosulys, dusulys kiti kvėpavimo sutrikimai ar skonio, kvapo nejautrumas, tada rekomenduojama pasidaryti covid-19 testą.',
            'kiek dienų inkubacinis periodas?':'Korona viruso inkubacinis periodas yra 14 dienų.',
            'kaip namuose saugotis nuo koronaviruso?': 'Turėtumėte ilsėtis, gerti daug skysčių ir valgyti maistingą maistą.',
            'ką daryti karščiuojant?': 'Kreipkitės į šeimos daktarą arba skambinkite numeriu - 1808.',
            'kur galiu sužinoti koronos testo atsakymą?': 'Atsakymas turėtu ateiti į el.paštą, sms žinute, o jeigu neatėjo galite patikrinti https: // www.esveikata.lt / puslapyje.'

        }

        # Assert
        for question, answer in testsmap.items():
            did_succeed = False
            try:
                result = list(list(look_for_answer(question).values())[0][1])[0]
            except:
                result = []
            print("Testing:",question)
            if answer == result:
                amount_succeded = amount_succeded + 1
                did_succeed = True
            if did_succeed:
                print("Result: Success")
            else:
                print("Result: Failed")
        print("Correct:",amount_succeded,"/",len(testsmap))
        #2021-01-05 rezultatas su 3, reitingo rezimu 9/32; su 2 - 5/32


        '''
                    inp = input().lower()
                    answers = look_for_answer(inp)
                    print(list(answers.keys()))
                    
            "kur prasidejo korona?": "pirmas COVID-19 atvėjis įvyko 2019 m. gruodį, Wuhan, Kinija",
            "kaip apsisaugoti nuo viruso?": "Lietuvos Respublikos sveikatos apsaugos ministerija skelbia, "
            "kad čiaudėjimas į alkunę yra veiksminga COVID-19 užsikrėtimų mažinimo "
            "priemonė",
            "ar galiu keliauti?": "pagal 2020-10-12 informacija, į kitas šalis galima keliauti, bet į kai kurias ("
            "kaip italija, kinija...) yra nerekomenduojama",
            "kokios spalvos mergaitės suknelė? ": "Atsiprašau, nežinau atsakymo į jūsų užduotą klausimą",
        '''


if __name__ == '__main__':
    unittest.main()
