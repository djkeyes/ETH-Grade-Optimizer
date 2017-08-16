from collections import OrderedDict
import time

import course_optimizer as co


def main():
    # Some general notes:
    # -Only one (non-interfocus) lab course can be counted. The optimization takes this into account, so label all your
    #  non-interfocus lab courses as such.
    # -Most courses that count as "Core Focus" or "Elective Focus" can also count for "Elective CS" or just "Elective",
    #  so label all your focus courses as electives, too
    # -On the other hand, most seminar courses can only count as a "Seminar in Focus". It's not really stated
    #  explicitly, but the department doesn't like it when you get a lot of seminar credits. So don't label those as
    #  electives.
    # -If you're a masochist and take all 3 interfocus labs, I'm not sure if you can count one as an elective or not.
    courses = [
        co.Course("Intro to FizzBuzz", 4.75, 8, co.Category.CORE_FOCUS, co.Category.ELECTIVE, co.Category.ELECTIVE_CS,
                  co.Category.ELECTIVE),
        co.Course("How to Design Manhole Covers", 4.0, 6, co.Category.CORE_FOCUS, co.Category.ELECTIVE_CS,
                  co.Category.ELECTIVE),
        co.Course("Twiddling Your Thumbs I", 5.25, 6, co.Category.ELECTIVE_FOCUS, co.Category.ELECTIVE_CS,
                  co.Category.ELECTIVE),
        co.Course("Twiddling Your Thumbs II", 5.5, 6, co.Category.ELECTIVE_FOCUS, co.Category.ELECTIVE_CS,
                  co.Category.ELECTIVE),
        co.Course("Advanced methods in FizzBuzzing", 5.25, 2, co.Category.SEMINAR_IN_FOCUS),
        co.Course("Information security Lab: Fuzzing Busily", 5.0, 10, co.Category.ELECTIVE_CS,
                  co.Category.ELECTIVE).lab(True),
        co.Course("P = NP, Just Set N=1", 4.25, 4, co.Category.ELECTIVE_CS, co.Category.ELECTIVE),
        co.Course("Support Vector Machine Guns", 4.75, 4, co.Category.ELECTIVE_CS, co.Category.ELECTIVE),
        co.Course("The Pass/Fail Course", None, 10, co.Category.ELECTIVE_CS,
                  co.Category.ELECTIVE).passfail(True),
        co.Course("Advanced computational algorithms lab", 4.0, 12, co.Category.INTERFOCUS),
        co.Course("Intro to Buzzsaws", 6.0, 8, co.Category.ELECTIVE),
        co.Course("Critical Analysis of the Bee Movie", 4.5, 6, co.Category.ELECTIVE),
        co.Course("FizzBuzz and society", 4.5, 2, co.Category.SCIENCE_IN_PERSPECTIVE),
        co.Course("Buzzing and Fizzing: What's next?", 5.5, 30, co.Category.THESIS),
    ]

    print('=========================================')
    print('Considering the following courses:')
    for c in courses:
        print('\t', c)
    print('=========================================')
    print('Optimizing!')
    start = time.time()
    result = co.optimize(courses)
    end = time.time()
    print('... complete! Optimization took', (end - start), 'seconds.')
    print('=========================================')

    if not result.possible:
        print('It looks like you don\'t have enough credits to graduate! :(')
        print(
            'Have you entered ALL your passed courses? This includes your thesis, GESS courses, and elective courses.')
    else:

        categories_to_names = OrderedDict()
        categories_to_names[co.Category.CORE_FOCUS] = "Core Focus"
        categories_to_names[co.Category.ELECTIVE_FOCUS] = "Elective Focus"
        categories_to_names[co.Category.SEMINAR_IN_FOCUS] = "Seminar in Focus"
        categories_to_names[co.Category.ELECTIVE_CS] = "Elective CS"
        categories_to_names[co.Category.INTERFOCUS] = "Interfocus"
        categories_to_names[co.Category.ELECTIVE] = "Elective"
        categories_to_names[co.Category.SCIENCE_IN_PERSPECTIVE] = "Science in Perspective (GESS)"
        categories_to_names[co.Category.THESIS] = "Master Thesis"

        print('Your best course assignments give a grade of', result.max_grade)
        print('(The worst grade encountered was', result.worst_grade, ')')
        print('Assign your courses to categories in the following way:')
        print('=========================================')
        for category, name in categories_to_names.items():
            course_list = result.assignments[category]
            print(name)
            if len(course_list) == 0:
                print('\t(none)')
            else:
                for course in course_list:
                    print('\t', course)
                    courses.remove(course)
        if len(courses) > 0:
            print('Mark these courses as "Performance Assessments without Category":')
            for course in courses:
                print('\t', course)
    print('\nHave a nice day.')


if __name__ == "__main__":
    main()
