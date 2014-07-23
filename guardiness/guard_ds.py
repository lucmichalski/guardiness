import logging
import datetime

"""This file holds guard-related data structures"""

class Guard(object):
    def __init__(self, guard_fpr, times_seen):
        """
        Initialize a guard node with identity fingerprint 'guard_fpr'
        that has appeared in 'times_seen' consensuses lately.
        """
        self.fingerprint = guard_fpr
        self.times_seen = times_seen

class Guards(object):
    """
    Keeps track of the guards we've encountered while parsing the various consensuses.
    """

    def __init__(self):
        # Keeps track of guards. Maps a <guard identity fpr> to a <Guard object>.
        self.guards = {}

    def register_guard(self, guard_fpr, times_seen):
        """Make a Guard object and keep track of it."""

        guard = Guard(guard_fpr, times_seen)
        self.guards[guard_fpr] = guard

    def _get_guard_guardfraction_percentage(self, guard, consensuses_read_n):
        """
        Calculate and return the guardfraction of 'guard'.

        Guardfraction is an integer percentage (a value in [0,100]) of
        how much this relay has been a guard according to the parsed
        consensuses.
        """

        guardfraction = guard.times_seen / float(consensuses_read_n)
        guardfraction_percentage = int(round(guardfraction*100))

        return guardfraction_percentage

    def write_output_file(self, output_fname, max_months, consensuses_read_n):
        """
        Write a guardfraction output file

        {{{
        written-at <date and time>
        n-inputs <number of consesuses parsed> <number of months considered>

        guard-seen <guard fpr 1> <guardfraction percentage> <number of consensus appearances>
        guard-seen <guard fpr 2> <guardfraction percentage> <number of consensus appearances>
        guard-seen <guard fpr 3> <guardfraction percentage> <number of consensus appearances>
        guard-seen <guard fpr 4> <guardfraction percentage> <number of consensus appearances>
        guard-seen <guard fpr 5> <guardfraction percentage> <number of consensus appearances>
        ...
        }}}

        Might raise IOError.
        """
        with open(output_fname, 'w+') as f:
            f_str = ""

            now = datetime.datetime.now()
            f_str += "written-at %s\n" % now.isoformat(sep=" ") # separate year from time with space
            f_str += "n-inputs %d %d\n" % (consensuses_read_n, max_months)

            sorted_guards = sorted(self.guards.values(), key=lambda x: x.times_seen, reverse=True)

            for guard in sorted_guards:
                f_str += "guard-seen %s %d %d\n" % (guard.fingerprint,
                        self._get_guard_guardfraction_percentage(guard, consensuses_read_n),
                        guard.times_seen)

            f.write(f_str)