from helpers import take, drop, first, rest
import os, sys, subprocess

def recursive_trie_branch(string, dictionary, should_return=False):
    '''Branch generates a branch in a trie. 
    This separation is necessary as there is a minor difference
    in <trie_branch> and <trie>. The difference being not returning from the 
    if statement or returning from the if statement for recursive purposes.

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
        dictionary[element] = trie_branch(rest(string), {})
        if should_return:
            return dictionary
    else:
        recursive_result = trie_branch(rest(string), dictionary.get(element))
        if should_return:
            return recursive_result

def trie_search(string, dictionary):
    '''I left the funky if and elif phrasing here (instead of an implicit else) 
    to reveal the symmetry between this and <recursive_trie_branch>. Using lisp
    macros would be an elegant solution to reducing all "3" trie functions.
    '''
    element = first(string)
    if not element in dictionary.keys():
        return False
    elif element in dictionary.keys():
        is_last_char = len(string) == 1
        is_terminal_char = dictionary.get(element) == {}
        if is_last_char and is_terminal_char:
            return True

        return trie_search(rest(string), dictionary.get(element))

def trie_branch(string, dictionary):
    '''Continue to recurse until the length of the given string is 0'''
    if len(string) == 0:
        return dictionary
    return recursive_trie_branch(string, dictionary, True)

    
def build_trie(lst, dictionary={}):
    '''<recursive_trie_branch> mutate the default dictionary, or optionally
    a pre-populated dictionary
    '''
    build_tree = [recursive_trie_branch(string, dictionary) for string in lst]
    return dictionary

def http_get_top_passwords():
    '''Retreive the top 1000 passwords using wget
    Read those passwords from a file and return them
    '''
    ### this isn't pep8? :O
    raw_text_url = 'https://raw.githubusercontent.com/DavidWittman/wpxmlrpcbrute/master/wordlists/1000-most-common-passwords.txt'
    file_name    = '1000-most-common-passwords.txt'

    #get
    get_pws = subprocess.run([
        'wget',
        '--no-check-certificate',
        '--content-disposition',
        raw_text_url], stderr=subprocess.DEVNULL)

    ### PASSWORDS ARE READ FROM A FILE!
    passwords = []
    with open(file_name, 'r') as f:
        passwords = [line for line in f.read().split('\n') if line]

    # cleanup environment
    os.remove(file_name)
    return passwords


def is_common_password(new_password, common_passwords=http_get_top_passwords()):
    tree = build_trie(common_passwords)
    return trie_search(new_password, tree)


if __name__ == '__main__':
    [_, test_password] = sys.argv
    print('Common Password' if is_common_password(test_password) else 'Not common password')




    












