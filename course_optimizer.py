from enum import Enum, unique


@unique
class Category(Enum):
    CORE_FOCUS = 1
    ELECTIVE_FOCUS = 2
    SEMINAR_IN_FOCUS = 3
    ELECTIVE_CS = 4
    INTERFOCUS = 5
    ELECTIVE = 6
    SCIENCE_IN_PERSPECTIVE = 7  # also known as GESS
    THESIS = 8


TOTAL_CREDITS_REQUIRED = 90
FOCUS_AND_ELECTIVE_CREDITS_REQUIRED = 36
FOCUS_CREDITS_REQUIRED = 26
CORE_FOCUS_CREDITS_REQUIRED = 10
SEMINAR_IN_FOCUS_CREDITS_REQUIRED = 2
ELECTIVE_CS_CREDITS_REQUIRED = 8
INTERFOCUS_CREDITS_REQUIRED = 12
GESS_CREDITS_REQUIRED = 2
THESIS_CREDITS_REQUIRED = 30


class CreditCounts:
    def __init__(self, total=0, focus_and_elective=0, focus=0, core_focus=0, seminar_in_focus=0, elective_cs=0,
                 interfocus=0, gess=0, thesis=0):
        self._total = total
        self._focus_and_elective = focus_and_elective
        self._focus = focus
        self._core_focus = core_focus
        self._seminar_in_focus = seminar_in_focus
        self._elective_cs = elective_cs
        self._interfocus = interfocus
        self._gess = gess
        self._thesis = thesis

    def add_assigned_course(self, category_assigned, credits):
        self._total += credits
        # PYTHON Y U NO SWITCH-CASE
        if category_assigned == Category.CORE_FOCUS:
            self._core_focus += credits
            self._focus += credits
            self._focus_and_elective += credits
        elif category_assigned == Category.ELECTIVE_FOCUS:
            self._focus += credits
            self._focus_and_elective += credits
        elif category_assigned == Category.SEMINAR_IN_FOCUS:
            self._seminar_in_focus += credits
            self._focus += credits
            self._focus_and_elective += credits
        elif category_assigned == Category.ELECTIVE_CS:
            self._elective_cs += credits
            self._focus_and_elective += credits
        elif category_assigned == Category.INTERFOCUS:
            self._interfocus += credits
        elif category_assigned == Category.ELECTIVE:
            pass
        elif category_assigned == Category.SCIENCE_IN_PERSPECTIVE:
            self._gess += credits
        elif category_assigned == Category.THESIS:
            self._thesis += credits

    def all_greater_than_or_equal(self, other):
        result = self._total >= other._total \
                 and self._focus_and_elective >= other._focus_and_elective \
                 and self._focus >= other._focus \
                 and self._core_focus > other._core_focus \
                 and self._seminar_in_focus >= other._seminar_in_focus \
                 and self._elective_cs >= other._elective_cs \
                 and self._interfocus >= other._interfocus \
                 and self._gess >= other._gess \
                 and self._thesis >= other._thesis
        return result

    def __str__(self):
        return 'counts: [' + str(self._total) + ', ' + str(self._focus_and_elective) + ', ' + str(
            self._focus) + ', ' + str(self._core_focus) + ', ' + str(self._seminar_in_focus) + ', ' + str(
            self._elective_cs) + ', ' + str(self._interfocus) + ', ' + str(self._gess) + ', ' + str(self._thesis) + ']'


MIN_CREDIT_COUNTS = CreditCounts(total=90, focus_and_elective=36, focus=26, core_focus=10, seminar_in_focus=2,
                                 elective_cs=8, interfocus=12, gess=2, thesis=30)


def create_credit_counts_from_assignments(assignments):
    counts = CreditCounts()

    for category, assigned in assignments.items():
        for course in assigned:
            counts.add_assigned_course(category, course.credits)
    return counts


def compute_weighted_avg_by_credits(courses):
    total_credits = 0.0
    total_grade = 0.0
    for course in courses:
        if course._is_passfail:
            continue
        total_credits += course.credits
        total_grade += course.credits * course.grade
    return total_grade / total_credits


def compute_grade(assignments):
    focus_avg = compute_weighted_avg_by_credits(
        assignments[Category.CORE_FOCUS] + assignments[Category.ELECTIVE_FOCUS] + assignments[
            Category.SEMINAR_IN_FOCUS])
    interfocus_avg = compute_weighted_avg_by_credits(assignments[Category.INTERFOCUS])
    elective_cs_avg = compute_weighted_avg_by_credits(assignments[Category.ELECTIVE_CS])
    thesis_avg = compute_weighted_avg_by_credits(assignments[Category.THESIS])

    return (3. * focus_avg + interfocus_avg + elective_cs_avg + 2. * thesis_avg) / (3. + 1. + 1. + 2.)


class Course:
    def __init__(self, name, grade, credits, *args):
        self._name = name
        self._grade = grade
        self._credits = credits
        self._categories = list(args)
        self._is_lab = False
        self._is_passfail = False

    def lab(self, is_lab):
        self._is_lab = is_lab
        return self

    def passfail(self, is_passfile):
        self._passfaile = is_passfile
        return self

    @property
    def categories(self):
        return self._categories

    @property
    def grade(self):
        return self._grade

    @property
    def credits(self):
        return self._credits

    def __str__(self):
        return self._name


class OptimizationResult:
    def __init__(self, possible, max_grade, assignments, worst_grade):
        self.possible = possible
        self.max_grade = max_grade
        self.assignments = assignments
        # Just for kicks:
        self.worst_grade = worst_grade


def optimize(courses):
    result = optimize_dfs(courses)
    return result


def copy_assignments(assignments):
    return {category: course_list.copy() for category, course_list in assignments.items()}


def optimize_dfs(courses, assignments={category: [] for category in Category}, has_lab=False):
    if len(courses) == 0:
        # TODO: check validity
        counts = create_credit_counts_from_assignments(assignments)
        if counts.all_greater_than_or_equal(MIN_CREDIT_COUNTS):
            grade = compute_grade(assignments)
            return OptimizationResult(True, grade, copy_assignments(assignments), grade)
        else:
            return OptimizationResult(False, None, None, None)

    counts = create_credit_counts_from_assignments(assignments)
    # might already be viable
    if counts.all_greater_than_or_equal(MIN_CREDIT_COUNTS):
        grade = compute_grade(assignments)
        best_result = OptimizationResult(True, grade, copy_assignments(assignments), grade)
    else:
        best_result = None

    cur_course = courses[0]
    remaining_courses = courses[1:]
    next_has_lab = has_lab or cur_course._is_lab
    # can't assign more than one lab
    if not cur_course._is_lab or not has_lab:
        # just try all the options
        for category in cur_course.categories:
            assignments[category].append(cur_course)
            cur_result = optimize_dfs(remaining_courses, assignments, next_has_lab)
            if best_result is None or not best_result.possible:
                best_result = cur_result
            elif cur_result.possible and cur_result.max_grade > best_result.max_grade:
                cur_result.worst_grade = min(cur_result.worst_grade, best_result.worst_grade)
                best_result = cur_result
            assignments[category].pop()

    # also consider not listing this course at all
    cur_result = optimize_dfs(remaining_courses, assignments, next_has_lab)
    if best_result is None or not best_result.possible:
        best_result = cur_result
    elif cur_result.possible and cur_result.max_grade > best_result.max_grade:
        cur_result.worst_grade = min(cur_result.worst_grade, best_result.worst_grade)
        best_result = cur_result

    return best_result
