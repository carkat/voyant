#!/bin/python
from helpers import take, drop, first, rest
import os,sys,subprocess

class PasswordTrie:
    '''Public methods:
    http_get_top_passwords
    build_trie
    trie_search
    is_last_char
    Private methods:
    _recursive_trie_branch
    _trie_branch
    '''
    def __init__(self):
        self.common_passwords = self.http_get_top_passwords()
        self.tree = self.build_trie(self.common_passwords)

    def _recursive_trie_branch(self, string, dictionary, should_return=False):
        '''Branch generates a branch in a trie. 
        There is symmetry between the bodies of:
        <_recursive_trie_branch>
        <trie_search>
        <_trie_branch>
        <build_trie>
        Sure wish I had lisp macros in python.

        There are 2 different outcomes:
        1. the element already exists, recurse on the existing value of dict[elem]
        - in this case, recursively generate the next branch
        2. the elment does not exist in the dictionary
        - add the key and recurse on a new empty dictionary
        Note: should_return prevents the need to duplicate essentially the same
        code in both <trie> and <trie_branch>. 
        '''
        element = first(string)
        if not element in dictionary.keys():
            dictionary[element] = self._trie_branch(rest(string), {})
            if should_return:
                return dictionary
        else:
            recursive_result = self._trie_branch(rest(string), dictionary.get(element))
            if should_return:
                return recursive_result

    def trie_search(self, string, dictionary):
        '''I left the funky if and elif phrasing here (instead of an implicit else) 
        to reveal the symmetry between this and <_recursive_trie_branch>. Using lisp
        macros would be an elegant solution to reducing all "3" trie functions.
        '''
        element = first(string)
        if not element in dictionary.keys():
            return False
        else:
            is_last_char = len(string) == 1
            is_terminal_char = dictionary.get(element) == {}
            if is_last_char and is_terminal_char:
                return True

            return self.trie_search(rest(string), dictionary.get(element))

    def _trie_branch(self,string, dictionary):
        if len(string) == 0:
            return dictionary
        return self._recursive_trie_branch(string, dictionary, True)

    
    def build_trie(self, lst, dictionary={}):
        '''<recursive_trie_branch> mutate the default dictionary, or optionally
        a pre-populated dictionary
        '''
        if type(lst) == str:
            lst=[lst]
        build_tree = [self._recursive_trie_branch(string, dictionary) for string in lst]
        return dictionary

                
    def http_get_top_passwords(self):
        '''Retreive the top 1000 passwords using wget
        '''
        # setup
        raw_text_url = 'https://raw.githubusercontent.com/DavidWittman/wpxmlrpcbrute/master/wordlists/1000-most-common-passwords.txt'
        file_name    = '1000-most-common-passwords.txt'
        
        #get
        get_pws = subprocess.run([
            'wget',
            '--no-check-certificate',
            '--content-disposition',
            raw_text_url], stderr=subprocess.DEVNULL)
        
        # read results from file
        passwords = []
        with open(file_name, 'r') as f:
            passwords = [line for line in f.read().split('\n') if line]
            
            # cleanup environment
        os.remove(file_name)
        return passwords
                    

    def is_common_password(self, new_password):
        return self.trie_search(new_password, self.tree)
    
if __name__ == '__main__':
    [_, test_password] = sys.argv
    pt = PasswordTrie()
    print('Common Password' if pt.is_common_password(test_password) else 'Not common password')






    











