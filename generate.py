from root_verb_tables.generate_table_for_root import load_templates
from root_verb_tables.generate_tag_for_roots import tag_root_3
from itertools import product

PRE = '_'
NON_PRE = '~'


def read_templates(filename):
    with open(filename, encoding='utf8') as f:
        proto = next(f).strip()
        templates = f.read()
    return proto, templates


def match(pattern, desired):
    if pattern == '_':
        return True
    return pattern == desired


def find_word(radicals, binyan, tense):
    definiteness = False
    plural = 'יחיד'
    voice = 'שלישי'
    templates = load_templates(radicals)
    # print()
    # print(radicals, binyan, tense, tag_root_3(radicals))
    male = None
    female = None
    for t_binyan, t_tense, t_voice, t_gender, t_plural, surface in templates:
        for gender in ['נקבה', 'זכר']:
            if match(t_binyan, binyan) and match(t_tense, tense) and match(t_voice, voice) and match(t_plural, plural):
                if match(t_gender, gender):
                    # print(t_binyan, t_tense, t_voice, t_gender, t_plural, surface, sep='\t')
                    # print('MATCH')
                    # print(  binyan,   tense,   voice,   gender,   plural, surface, sep='\t')
                    if gender == 'נקבה':
                        if female: assert False
                        female = surface
                    elif gender == 'זכר':
                        if male: assert False
                        male = surface
    if male == female or female is None or male is None:
        return '', ''
    return male, female


def instantiate_all(item):
    with open('disambiguator_roots.txt', encoding='utf8') as f:
        disambiguator_roots = [root.split('.') for root in f.read().split('\n') if root.strip()]

    sentence = item['sentence']
    print(item['target-occupation'])
    for occupation in item['target-occupation']:
        for definiteness in item['target-def']:
            if definiteness:
                def_occupation = 'ה' + occupation
            else:
                def_occupation = occupation
            sentence_occupied = sentence.replace('@', def_occupation)
            for dis_binyan, dis_tense in product(item['disambig-binyan'], item['disambig-tense']):
                for dis_radicals in disambiguator_roots:
                    male, female = find_word(dis_radicals, dis_binyan, dis_tense)
                    if not female or not male:
                        continue
                    male, female = sentence_occupied.replace('$', male), sentence_occupied.replace('$', female)
                    yield male, female


if __name__ == '__main__':
    import json
    with open('templates.json', encoding='utf8') as f:
        templates = json.load(f)
        print(templates)
    for male, female in instantiate_all(templates):
        print(male)
        print(female)
        print()
    # print(list(find_word(list('אכל'), 'נפעל', 'עבר')))
