import unittest

import course_optimizer as co


def create_minimal_course_list(default_grade=5.0):
    courses = [
        co.Course("Intro to FizzBuzz", default_grade, 24, co.Category.CORE_FOCUS, co.Category.ELECTIVE,
                  co.Category.ELECTIVE_CS,
                  co.Category.ELECTIVE),
        co.Course("Advanced methods in FizzBuzzing", default_grade, 2, co.Category.SEMINAR_IN_FOCUS),
        co.Course("Information security: Fuzzing Busily", default_grade, 10, co.Category.ELECTIVE_CS,
                  co.Category.ELECTIVE),
        co.Course("Advanced computational algorithms lab", default_grade, 12, co.Category.INTERFOCUS),
        co.Course("Intro to Buzzsaws?", default_grade, 10, co.Category.ELECTIVE),
        co.Course("FizzBuzz and society", default_grade, 2, co.Category.SCIENCE_IN_PERSPECTIVE),
        co.Course("Buzzing and Fizzing: What's next?", default_grade, 30, co.Category.THESIS),
    ]
    return courses


class OptimizerTests(unittest.TestCase):
    def testTrivialSolutions(self):
        courses = create_minimal_course_list(4.0)
        result = co.optimize(courses)
        self.assertTrue(result.possible)
        self.assertAlmostEquals(result.max_grade, 4.0)
        self.assertEqual(len(result.assignments[co.Category.CORE_FOCUS]), 1)
        self.assertEqual(len(result.assignments[co.Category.ELECTIVE_FOCUS]), 0)
        self.assertEqual(len(result.assignments[co.Category.SEMINAR_IN_FOCUS]), 1)
        self.assertEqual(len(result.assignments[co.Category.ELECTIVE_CS]), 1)
        self.assertEqual(len(result.assignments[co.Category.INTERFOCUS]), 1)
        self.assertEqual(len(result.assignments[co.Category.ELECTIVE]), 1)
        self.assertEqual(len(result.assignments[co.Category.SCIENCE_IN_PERSPECTIVE]), 1)
        self.assertEqual(len(result.assignments[co.Category.THESIS]), 1)

    def testInsufficientCreditsDetected(self):
        courses = []
        result = co.optimize(courses)
        self.assertFalse(result.possible)

        courses = create_minimal_course_list()
        # removing any one of these should fail
        for i in range(len(courses)):
            result = co.optimize(courses[:i] + courses[i + 1:])
            self.assertFalse(result.possible)

        courses = create_minimal_course_list()
        result = co.optimize(courses)
        self.assertTrue(result.possible)

    def testInsufficientFocusCredits(self):
        courses = create_minimal_course_list(4.0)
        courses = [course for course in courses if co.Category.CORE_FOCUS not in course._categories]
        courses.append(co.Course("asdf", 4.0, 23, co.Category.CORE_FOCUS))
        result = co.optimize(courses)

        self.assertFalse(result.possible)
        courses.append(co.Course("qwerty", 4.0, 1, co.Category.ELECTIVE_FOCUS))
        result = co.optimize(courses)
        self.assertTrue(result.possible)
        self.assertAlmostEquals(result.max_grade, 4.0)

    def testInsufficientFocusAndElectiveCredits(self):
        default_grade = 4.0
        courses = [
            co.Course("CF", default_grade, 24, co.Category.CORE_FOCUS, co.Category.ELECTIVE,
                      co.Category.ELECTIVE_CS,
                      co.Category.ELECTIVE),
            co.Course("SF", default_grade, 2, co.Category.SEMINAR_IN_FOCUS),
            co.Course("ECS", default_grade, 9, co.Category.ELECTIVE_CS,
                      co.Category.ELECTIVE),
            co.Course("IF", default_grade, 12, co.Category.INTERFOCUS),
            co.Course("EL", default_grade, 10, co.Category.ELECTIVE),
            co.Course("SIP", default_grade, 2, co.Category.SCIENCE_IN_PERSPECTIVE),
            co.Course("MT", default_grade, 30, co.Category.THESIS),
        ]
        result = co.optimize(courses)
        self.assertFalse(result.possible)
        courses.append(co.Course("ECS2", default_grade, 1, co.Category.ELECTIVE_CS, co.Category.ELECTIVE))
        result = co.optimize(courses)
        self.assertTrue(result.possible)
        self.assertAlmostEquals(result.max_grade, 4.0)

    def testInsufficientTotalCredits(self):
        default_grade = 4.0
        courses = [
            co.Course("CF", default_grade, 24, co.Category.CORE_FOCUS, co.Category.ELECTIVE,
                      co.Category.ELECTIVE_CS,
                      co.Category.ELECTIVE),
            co.Course("SF", default_grade, 2, co.Category.SEMINAR_IN_FOCUS),
            co.Course("ECS", default_grade, 10, co.Category.ELECTIVE_CS,
                      co.Category.ELECTIVE),
            co.Course("IF", default_grade, 12, co.Category.INTERFOCUS),
            co.Course("EL", default_grade, 9, co.Category.ELECTIVE),
            co.Course("SIP", default_grade, 2, co.Category.SCIENCE_IN_PERSPECTIVE),
            co.Course("MT", default_grade, 30, co.Category.THESIS),
        ]
        result = co.optimize(courses)
        self.assertFalse(result.possible)
        courses.append(co.Course("EL2", default_grade, 1, co.Category.ELECTIVE))
        result = co.optimize(courses)
        self.assertTrue(result.possible)
        self.assertAlmostEquals(result.max_grade, 4.0)

    def testTwoOptions(self):
        courses = create_minimal_course_list(4.0)
        result = co.optimize(courses)
        self.assertTrue(result.possible)
        self.assertAlmostEquals(result.max_grade, 4.0)

        better_courses = [
            co.Course("Better core focus", 6.0, 24, co.Category.CORE_FOCUS, co.Category.ELECTIVE,
                      co.Category.ELECTIVE_CS, co.Category.ELECTIVE),
            co.Course("Better seminar", 6.0, 2, co.Category.SEMINAR_IN_FOCUS),
            co.Course("Better elective", 6.0, 10, co.Category.ELECTIVE_CS, co.Category.ELECTIVE),
            co.Course("Better interfocus", 6.0, 12, co.Category.INTERFOCUS),
            co.Course("Better gess", 6.0, 2, co.Category.SCIENCE_IN_PERSPECTIVE),
        ]
        expected_grades = [
            (3 * (6 * 24 + 4 * 2) / 26 + 4 + 4 + 2 * 4) / 7,
            (3 * (4 * 24 + 6 * 2) / 26 + 4 + 4 + 2 * 4) / 7,
            (3 * 4 + 6 + 4 + 2 * 4) / 7,
            (3 * 4 + 4 + 6 + 2 * 4) / 7,
            (3 * 4 + 4 + 4 + 2 * 4) / 7,  # gess has no effect
        ]

        for better_course, expected_grade in zip(better_courses, expected_grades):
            better_result = co.optimize(courses + [better_course])
            self.assertTrue(better_result.possible)
            self.assertAlmostEquals(better_result.max_grade, expected_grade)

    def testWhenBetterToRedistribute(self):
        courses = create_minimal_course_list(4.0)
        result = co.optimize(courses)
        self.assertTrue(result.possible)
        self.assertAlmostEquals(result.max_grade, 4.0)

        # in this case, it's better to count one core focus as the main core focus, and use the other to replace
        # elective cs
        bcf1 = co.Course("Better core focus 1", 6.0, 24, co.Category.CORE_FOCUS, co.Category.ELECTIVE,
                         co.Category.ELECTIVE_CS, co.Category.ELECTIVE)
        bcf2 = co.Course("Better core focus 2", 6.0, 24, co.Category.CORE_FOCUS, co.Category.ELECTIVE,
                         co.Category.ELECTIVE_CS, co.Category.ELECTIVE)

        better_result = co.optimize(courses + [bcf1, bcf2])
        self.assertTrue(better_result.possible)
        self.assertGreater(better_result.max_grade, result.max_grade)
        self.assertAlmostEquals(better_result.max_grade, (3 * (6 * 24 + 4 * 2) / 26 + 6 + 4 + 2 * 4) / 7)

    def testCantUseTwoLabs(self):
        default_grade = 4.0
        courses = [
            co.Course("CF", default_grade, 24, co.Category.CORE_FOCUS, co.Category.ELECTIVE, co.Category.ELECTIVE_CS,
                      co.Category.ELECTIVE),
            co.Course("SF", default_grade, 2, co.Category.SEMINAR_IN_FOCUS),
            co.Course("ECS1", default_grade, 10, co.Category.ELECTIVE_CS).lab(True),
            co.Course("ECS2", default_grade, 10, co.Category.ELECTIVE_CS, co.Category.ELECTIVE).lab(True),
            co.Course("IF", default_grade, 12, co.Category.INTERFOCUS),
            co.Course("SIP", default_grade, 2, co.Category.SCIENCE_IN_PERSPECTIVE),
            co.Course("MT", default_grade, 30, co.Category.THESIS),
        ]
        result = co.optimize(courses)
        self.assertFalse(result.possible)


def main():
    unittest.main()


if __name__ == '__main__':
    main()
