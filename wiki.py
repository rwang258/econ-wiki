import wikipedia
import csv

input_file = csv.DictReader(open("Final_top_don_501_1000_copy.csv"))

with open('final_names_output_2.csv', 'w') as f:
    # initialize output file
    fieldnames = ['contributor.name', 'Birth date',
                  'Birth state', 'Death date', 'Death state', 'Source']
    writer = csv.DictWriter(f, fieldnames=fieldnames)

    # for each name
    for row in input_file:
        # get the name
        orig_name = row['contributor.name']
        strl = orig_name.split(", ")
        first = strl[1]
        last = strl[0]
        name = first + " " + last

        # get the sentence with the dates for that name
        titles = wikipedia.search(name, results=1)

        if len(titles) == 0:
            writer.writerow({'contributor.name': orig_name, 'Birth date': 'NA',
                             'Birth state': 'NA', 'Death date': 'NA',
                             'Death state': 'NA', 'Source': 'NA'})
            continue
        else:
            # get the actual title
            title = titles[0]
            try:
                dateSentence = wikipedia.summary(
                    title, sentences=1, auto_suggest=False, redirect=True)
            except wikipedia.DisambiguationError as e:
                dateSentence = wikipedia.summary(
                    e.options[0], sentences=1, auto_suggest=False, redirect=True)

        # print(dateSentence)

        # get the dates
        date = dateSentence[dateSentence.find("(")+1:dateSentence.find(")")]

        # find index of -
        dash = date.find("-")

        birthDate = ""
        deathDate = ""
        # if only birth date is found
        if dash == -1:
            bornFound = date.find("born")
            if bornFound == -1:
                writer.writerow({'contributor.name': orig_name, 'Birth date': 'NA',
                                 'Birth state': 'NA', 'Death date': 'NA',
                                 'Death state': 'NA', 'Source': 'NA'})
                continue
            birthDate = date[bornFound+5:]

        # if both dates found
        else:
            birthDate = date[:dash-1]
            deathDate = date[dash+2:]

        # get page url
        try:
            pg = wikipedia.page(title, auto_suggest=False, redirect=True)
        except wikipedia.DisambiguationError as e:
            pg = wikipedia.page(
                e.options[0], auto_suggest=False, redirect=True)
        source = pg.url

        # input into output file
        # if only birth date
        if dash == -1:
            writer.writerow({'contributor.name': orig_name, 'Birth date': birthDate,
                             'Birth state': 'NA', 'Death date': 'NULL',
                             'Death state': 'NULL', 'Source': source})
        # if both dates found
        else:
            writer.writerow({'contributor.name': orig_name, 'Birth date': birthDate,
                             'Birth state': 'NA', 'Death date': deathDate,
                             'Death state': 'NA', 'Source': source})

# print(wikipedia.summary("Donald Trump", sentences=2))
# print(wikipedia.search("aljasdfklj 892"))
# print(wikipedia.search("dave group"))
