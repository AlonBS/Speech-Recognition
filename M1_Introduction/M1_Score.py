import argparse
import wer
import re


def __format_str(num1, num2):

    return ("{0:.1f}%".format(num1/num2 *100))

def __build_trans(fileName):

    dic = {}
       
    with open(fileName) as file:
        for line in file:
            entry = re.search('([\w ]+ )(\([0-9-]+\))', line)
            if entry:
                dic[entry.group(2).strip('()')] = entry.group(1).strip()
   
    return dic
    

def build_transcriptions_dics(ref_trn, hyp_trn):

    return __build_trans(ref_trn), __build_trans(hyp_trn)
   
            
        
        
        
        
            

# create a function that calls wer.string_edit_distance() on every utterance
# and accumulates the errors for the corpus. Then, report the word error rate (WER)
# and the sentence error rate (SER). The WER should include the the total errors as well as the
# separately reporting the percentage of insertions, deletions and substitutions.
# The function signature is
# num_tokens, num_errors, num_deletions, num_insertions, num_substitutions = wer.string_edit_distance(ref=reference_string, hyp=hypothesis_string)
def score(ref_trn=None, hyp_trn=None):

    ref_trn_dic, hyp_trn_dic = build_transcriptions_dics(ref_trn, hyp_trn)
    
    total_num_of_words = 0
    total_num_of_ref_sent = len(ref_trn_dic)
    sentences_with_errors = 0
    total_errors = 0
    total_substitutions, total_insertions, total_deletions = 0,0,0
    
    
    for (key, value) in hyp_trn_dic.items():
        reference_string = ref_trn_dic[key]
        hypothesis_string = value
        for ref_word, hyp_word in zip(reference_string.split(), hypothesis_string.split()):
            
            num_tokens, num_errors, num_deletions, num_insertions, num_substitutions = wer.string_edit_distance(ref=ref_word, hyp=hyp_word)
                    
            total_num_of_words += num_tokens
            total_errors += num_errors
            total_deletions += num_deletions
            total_insertions += num_insertions
            total_substitutions += num_substitutions
               
            if num_errors > 0:
                sentences_with_errors +=1
    
    print ()
    print ("====================================================================")
    print("Total number of reference sentences: " + str(total_num_of_ref_sent))
    print("Num of sentences with error: " + str(sentences_with_errors))
    print("SER: " + __format_str(total_num_of_ref_sent, sentences_with_errors))
    
    print()
    print ("Total number of:")
    print ("\tWords: " + str(total_num_of_words))
    print ("\tErrors: " + str(total_errors))
    print ("\tDeletions: " + str(total_deletions))
    print ("\tInsertions: " + str(total_insertions))
    print ("\tSubstitutions: " + str(total_substitutions))
    
    print ("WER: " + __format_str(total_substitutions + total_insertions + total_deletions, total_num_of_words))
    print ("====================================================================")
  

    return

if __name__=='__main__':
    parser = argparse.ArgumentParser(description="Evaluate ASR results.\n"
                                                 "Computes Word Error Rate and Sentence Error Rate")
    parser.add_argument('-ht', '--hyptrn', help='Hypothesized transcripts in TRN format', required=True, default=None)
    parser.add_argument('-rt', '--reftrn', help='Reference transcripts in TRN format', required=True, default=None)
    args = parser.parse_args()

    if args.reftrn is None or args.hyptrn is None:
        RuntimeError("Must specify reference trn and hypothesis trn files.")

    score(ref_trn=args.reftrn, hyp_trn=args.hyptrn)

