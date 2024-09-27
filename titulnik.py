from docxtpl import DocxTemplate


def titulnik(data):
    fio = data.split('\n')[0]
    group = data.split('\n')[1]
    person = data.split('\n')[2]
    napr = data.split('\n')[3]
    title = data.split('\n')[4]

    doc = DocxTemplate("шаблон.docx")
    context = {"fio": fio, 'group': group, 'person': person, 'napr': napr, 'title': title}

    doc.render(context)
    doc.save(f"titulnik_{person.split('.')[2]}.docx")
    return f"titulnik_{person.split('.')[2]}.docx"

