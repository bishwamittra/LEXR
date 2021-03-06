from time import time


class TableTimedOut(Exception):
    pass


class ObservationTable:
    def __init__(self, alphabet, interface, max_table_size=None):
        self.S = {""}  # starts. invariant: prefix closed
        self.E = {""}  # ends. invariant: suffix closed
        # {} #T: (S cup (S dot A)) dot E -> {True,False}, might also have more info if
        self.T = interface.recorded_words
        # interface remembers more, but this is not harmful so long as it contains what it needs
        self.A = alphabet  # alphabet
        self.interface = interface
        self._fill_T()
        self._initiate_row_equivalence_cache()
        self.max_table_size = max_table_size
        self.time_limit = None

    def set_time_limit(self, time_limit, start):
        self.time_limit = time_limit
        self.start = start

    # modifies, and involved in every kind of modification. modification: store more words
    def _fill_T(self, new_e_list=None, new_s=None):
        self.interface.update_words(self._Trange(new_e_list, new_s))

    # T: (S cup (S dot A)) dot E -> {True,False} #doesn't modify
    def _Trange(self, new_e_list, new_s):
        E = self.E if None is new_e_list else new_e_list
        starts = self.S | self._SdotA() if None is new_s else [
            new_s+a for a in (list(self.A)+[""])]
        return set([s+e for s in starts for e in E])

    def _SdotA(self):  # doesn't modify
        return set([s+a for s in self.S for a in self.A])

    def _initiate_row_equivalence_cache(self):
        self.equal_cache = set()  # subject to change
        for s1 in self.S:
            for s2 in self.S:
                for a in list(self.A)+[""]:
                    if self._rows_are_same(s1+a, s2):
                        self.equal_cache.add((s1+a, s2))

    # just fixes cache. in case of new_e - only makes it smaller
    def _update_row_equivalence_cache(self, new_e=None, new_s=None):
        if not None is new_e:
            remove = [
                (s1, s2) for s1, s2 in self.equal_cache if not self.T[s1+new_e] == self.T[s2+new_e]]
            self.equal_cache = self.equal_cache.difference(remove)
        else:  # new_s != None, or a bug!
            for s in self.S:
                for a in (list(self.A) + [""]):
                    if self._rows_are_same(s+a, new_s):
                        self.equal_cache.add((s+a, new_s))
                    if self._rows_are_same(new_s+a, s):
                        self.equal_cache.add((new_s+a, s))

    def _rows_are_same(self, s, t):  # doesn't modify
        # row(s) = f:E->{0,1} where f(e)=T(se)
        return None is next((e for e in self.E if not self.T[s+e] == self.T[t+e]), None)

    def all_live_rows(self):
        return [s for s in self.S if s == self.minimum_matching_row(s)]

    def minimum_matching_row(self, t):  # doesn't modify
        # to be used by automaton constructor once the table is closed
        # not actually minimum length but so long as we're all sorting them by something then whatever
        try:
            return next(s for s in self.S if (t, s) in self.equal_cache)
        except:
            print(self.S)
            print(t)
            # print(self.equal_cache)
            # print(s for s in self.S if (t, s) in self.equal_cache)
            raise ValueError



    def timed_out(self):
        if not None is self.time_limit:
            time_taken = time()-self.start
            if time_taken > self.time_limit:
                print("obs table timed out")
                print("Total time taken:", time_taken)
                return False
                # raise TableTimedOut() # whatever, can't be bothered rn
        return True

    # modifies - and whenever it does, calls _fill_T
    def find_and_handle_inconsistency(self):
        # returns whether table was inconsistent
        maybe_inconsistent = [(s1, s2, a) for s1, s2 in self.equal_cache if s1 in self.S for a in self.A
                              if not (s1+a, s2+a) in self.equal_cache]
        troublemakers = [a+e for s1, s2, a in maybe_inconsistent for e in
                         [next((e for e in self.E if not self.T[s1+a+e] == self.T[s2+a+e]), None)] if not None is e]
        if len(troublemakers) == 0:
            return False
        self.E.add(troublemakers[0])
        # optimistic batching for queries - (hopefully) most of these will become relevant later
        self._fill_T(new_e_list=troublemakers)
        self._update_row_equivalence_cache(troublemakers[0])
        # self._assert_not_timed_out()
        return True

    def find_and_close_row(self):  # modifies - and whenever it does, calls _fill_T
        # returns whether table was unclosed
        s1a = next((s1+a for s1 in self.S for a in self.A if not [
                   s for s in self.S if (s1+a, s) in self.equal_cache]), None)
        if None is s1a:
            return False
        self.S.add(s1a)
        self._fill_T(new_s=s1a)
        self._update_row_equivalence_cache(new_s=s1a)
        # self._assert_not_timed_out()
        return True

    # modifies - and definitely calls _fill_T
    def add_counterexample(self, ce, label):
        if ce in self.S:
            # print("bad counterexample - already saved and classified in table!")
            return

        # print("counterexample: ---->", ce)
        ce_split = None
        if("x" in ce):
            ce_split = [ "x" + c for c in ce.split("x")[1:]]
        else:
            ce_split = ce

        new_states = [("").join(ce_split[0:i+1])
                      for i in range(len(ce_split)) if not ("").join(ce_split[0:i+1]) in self.S]

        # print(new_states)
        # print("Got new states:", new_states)
        # print("Previous states:", self.S)
        self.T[ce] = label
        self.S.update(new_states)

        self._fill_T()  # has to be after adding the new states
        for s in new_states:  # has to be after filling T
            self._update_row_equivalence_cache(new_s=s)
        # self._assert_not_timed_out()

