import spacy
from pro_utils.read_files import read_txt_files

# nlp = spacy.load('es')
nlp = spacy.load("es_core_news_md")


def ner_api_test(qa_span_list, qa_chi_list):
    nlp = spacy.load('es')
    location_info = []
    for key, ele in enumerate(qa_span_list):
        test_sent = nlp(ele)
        for ent in test_sent.ents:
            if ent.label_ == "ORG" and (ent.text not in location_info):
                location_info.append(ent.text)
                # print('the sentence is : ', ele)
                # print('the trans sentence is : ', qa_chi_list[key])
                # print(ent, ent.label_, ent.label)
            else:
                pass
    return location_info


def similar_api_test(sentence_1, sentence_2):
    test_1 = nlp(sentence_1)
    test_2 = nlp(sentence_2)
    similarity = test_1.similarity(test_2)
    print(similarity)
    return 0


if __name__ == "__main__":
    # for i in range(1, 13):
    #     name = str(i) + '.txt'
    #     span_name = str(i) + '_span.txt'
    #     read_span_lines = read_txt_files(span_name)
    #     read_chi_lines = read_txt_files(name)
    #     loc = ner_api_test(read_span_lines, read_chi_lines)
    #     print(loc)
    #     print('the ', i, ' docx extraction is over')

    # for_1 = "QUITO GRAN COLOMBIA Y  YAGUACHI FRENTE A HOSPITAL EUGENIO ESPEJO ALERTANTE INFORMA " \
    #         "QUE DE UN BUS SE CAYO TANQUE DE DIESEL ESTA REGADO POR TODA LA CALLE SOLICITA BOMBEROS"
    # for_2 = "PRO/ R/ DIR: GRAN COLOMBIA-YAHUACHI N15B REF: FRENTE SAMBLEA NACIONAL ALERTANTE INDICA QUE HAY " \
    #         " UN BUS DE LA LINEA NACIONAL SUCRE QUE SE LE CAYO EL TANQUE DE COMBUSTIBLE Y SE ESTA DERRAMANDO" \
    #         " EL COMBUSTIBLE EN EL ASFALTO"
    # for_3 = "CANTON/ QUITO DIR/ GRAN COLOMBIA-YAHUACHI N15B REF/ SALIDA NORTE DEL HOSPITAL  EUGENIO ESPEJO " \
    #         "EL ALERTANTE INDICA/ REGADO COMBUSTIBLE EN LA VIA DIESEL"
    # for_4 = "CANTON/ QUITO DIR/ GRAN COLOMBIA-YAHUACHI N15B REF/ SALIDA NORTE DEL HOSPITAL  " \
    #         "EUGENIO ESPEJO EL ALERTANTE INDICA/ REGADO COMBUSTIBLE EN LA VIA DIESEL"
    # for_5 = "R/ QUITO DIRECCION/ AV INTEROCEANICA REF/ CERCA DEL MERCADO DEL ARENAL FRENTE AL CHICHE INCIDENTE/ " \
    #         "ALARMANTE INDICA ACCIDENTE DE MOTO 1 PERSONA HERIDA ESTA INCONSIENTE SE ENCUENTRA SANGRANDO"
    # for_6 = "P/ PICHINCHA DIR/ SECTOR DEL ARENAL REF/ JUNTO AL MERCADO SECTOR/  TUMBACO EL ALERTANTE INDICA QUE HAY " \
    #         "UNA PERSONA ATROPELLADA NO SABE SI ESTA HERIDO YA QUE PASABA POR AHI"

    # t_1 = 'ALERTANTE INFORMA QUE DE UN BUS SE CAYO TANQUE DE DIESEL ESTA REGADO POR TODA LA CALLE SOLICITA BOMBEROS.'
    # t_2 = 'ALERTANTE INDICA QUE HAY  UN BUS DE LA LINEA NACIONAL SUCRE QUE SE LE CAYO EL TANQUE DE COMBUSTIBLE Y SE ' \
    #       'ESTA DERRAMANDO EL COMBUSTIBLE EN EL ASFALTO'
    # t_3 = 'EL ALERTANTE INDICA/ REGADO COMBUSTIBLE EN LA VIA DIESEL'
    #
    # q_1 = 'INCIDENTE/ ALARMANTE INDICA ACCIDENTE DE MOTO 1 PERSONA HERIDA ESTA INCONSIENTE SE ENCUENTRA SANGRANDO'
    # q_2 = 'EL ALERTANTE INDICA QUE HAY UNA PERSONA ATROPELLADA NO SABE SI ESTA HERIDO YA QUE PASABA POR AHI'
    # similar_api_test(t_1, t_2)

    tt_1 = 'KM 62 VIA AL TENA BARRIO SANTA ROSA SRA ENVENENADA SE ENCUENTRA EN LA COMUNIDAD ' \
           'COTICUTANA NECESITA AYUDA URGENTE'
    tt_2 = 'TIENDA AL FRENTE. ' \
           'CASA COLOR BLANCO CON TOMATE SEÑORA ENVENEDADA CONCIENTE, RESPIRANDO'

    qq_1 = 'VIA PANA COMPLEJO TURISTICO ALERTANTE INDICA QUE HAY 4 SOSPECHOSOS AFROECUATORINOS ' \
           'RONDANDO SU LOCAL LICORERIA SIENTE COMO QUE LE QUIEREN ASALTAR NO HAY NOMBRE EN CALLES RAZA NEGRA 4'
    qq_2 = 'VIA PANA A 500M DE LAS ORQUIDIAS EN LOCAL BOTATE AL AGUA EL ALERTANTE INDICA QUE ' \
           'UNA BANDA DE DELINCUENTES VA A INGRESAR AL LOCAL A DELINQUIR UNO DE LOS SOSPECHOSOS VISTE ' \
           'CAMISA BLANCA Y PANTALON AZUL'

    similar_api_test(tt_1, tt_2)