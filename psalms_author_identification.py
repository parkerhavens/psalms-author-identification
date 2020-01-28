import re


def main():
    chapters = clean_psalms()

    write_cleaned_chapters(chapters)

    chapters_by_david, chapters_by_others, chapters_by_unknown = get_chapters_by_authors(chapters)

    print(len(chapters_by_david))


def clean_psalms():

    psalms = open('psalms.txt', 'r')

    content = psalms.read()

    content_no_selah = content.replace('\n\nSelah\n\n', '\nSelah\n')

    content_no_verses = re.sub('[0-9]{1,3}:[0-9]{1,3} ', '', content_no_selah)

    # doesn't work
    content_no_books = re.sub('BOOK+\n', '', content_no_verses)

    content_no_single_lines = re.sub('\n(?:(?!ab).)\n\n', '', content_no_books)

    content_split_on_chapter = re.split('\nPsalm [0-9]{1,3}\n', content_no_single_lines)

    chapters_cleaned = []

    for chapter in content_split_on_chapter[1:]:

        lines = chapter.splitlines()

        chapter_no_title = ""

        if lines[2] == "":
            chapter_no_title += "\n".join(lines[2:])
        else:
            chapter_no_title += "\n".join(lines)

        chapters_cleaned.append(chapter_no_title)

    psalms.close()

    return chapters_cleaned


def write_cleaned_chapters(chapters_cleaned):
    psalms_cleaned = open('psalms_cleaned.txt', "w+")

    for chapter in chapters_cleaned:
        psalms_cleaned.write(chapter)
        psalms_cleaned.write('\n\n---------------------------------------------------------------\n')

    psalms_cleaned.close()


def get_chapters_by_authors(chapters):
    david_indexes_file = open('david_indexes.txt', 'r')
    others_indexes_file = open('others_indexes.txt', 'r')

    david_indexes = david_indexes_file.read().split("\n")
    others_indexes = others_indexes_file.read().split("\n")

    chapters_by_david = []
    chapters_by_others = []
    chapters_by_unknown = []

    for index, chapter in enumerate(chapters):
        if str(index + 1) in david_indexes:
            #print("David!")
            chapters_by_david.append(chapter)
        elif str(index + 1) in others_indexes:
            #print("Other!")
            chapters_by_others.append(chapter)
        else:
            #print("Unknown!")
            chapters_by_unknown.append(chapter)

    return chapters_by_david, chapters_by_others, chapters_by_unknown


if __name__ == "__main__":
    main()
