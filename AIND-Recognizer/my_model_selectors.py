import math
import statistics
import warnings

import numpy as np
from hmmlearn.hmm import GaussianHMM
from sklearn.model_selection import KFold
from asl_utils import combine_sequences


class ModelSelector(object):
    '''
    base class for model selection (strategy design pattern)
    '''

    def __init__(self, all_word_sequences: dict, all_word_Xlengths: dict, this_word: str,
                 n_constant=3,
                 min_n_components=2, max_n_components=10,
                 random_state=14, verbose=False):
        self.words = all_word_sequences
        self.hwords = all_word_Xlengths
        self.sequences = all_word_sequences[this_word]
        self.X, self.lengths = all_word_Xlengths[this_word]
        self.this_word = this_word
        self.n_constant = n_constant
        self.min_n_components = min_n_components
        self.max_n_components = max_n_components
        self.random_state = random_state
        self.verbose = verbose

    def select(self):
        raise NotImplementedError

    def base_model(self, num_states):
        # with warnings.catch_warnings():
        warnings.filterwarnings("ignore", category=DeprecationWarning)
        # warnings.filterwarnings("ignore", category=RuntimeWarning)
        try:
            hmm_model = GaussianHMM(n_components=num_states, covariance_type="diag", n_iter=1000,
                                    random_state=self.random_state, verbose=False).fit(self.X, self.lengths)
            if self.verbose:
                print("model created for {} with {} states".format(self.this_word, num_states))
            return hmm_model
        except:
            if self.verbose:
                print("failure on {} with {} states".format(self.this_word, num_states))
            return None


class SelectorConstant(ModelSelector):
    """ select the model with value self.n_constant

    """

    def select(self):
        """ select based on n_constant value

        :return: GaussianHMM object
        """
        best_n_components = self.n_constant
        return self.base_model(best_n_components)


class SelectorBIC(ModelSelector):
    """ select the model with the lowest Bayesian Information Criterion(BIC) score

    http://www2.imm.dtu.dk/courses/02433/doc/ch6_slides.pdf
    Bayesian information criteria: BIC = -2 * logL + p * logN
    """

    def select(self):
        """ select the best model for self.this_word based on
        BIC score for n between self.min_n_components and self.max_n_components

        :return: GaussianHMM object
        """
        warnings.filterwarnings("ignore", category=DeprecationWarning)
        #TODO implement model selection based on BIC scores
        #Every model has a BIC score and we want to select the best model.
        #The best model is the model with the smallest BIC score.
        #As explained here: www.stanfordphd.com/BIC.html
        #Procedure is as follows:
        #Loop from min_n_components to max_n_components
        #fit for each n_component with GaussianHMM(...).fit(...) to get model & logL
        #Compute BIC value for each model
        #return model with the smallest BIC value
        best_n_components = 0 #best number of states /best n_components
        init_score = float('inf') #choose best score to be an arbitrary large number e.g +inf
        N = self.X.shape[0]  #Number of data points/samples
        #N = len(self.X)  # Number of samples
        for n_component in range(self.min_n_components, self.max_n_components+1):
            try:
                #candidate model
                candidate_model = self.base_model(n_component)
                logL = candidate_model.score(self.X, self.lengths)  # Get logLikelihood
                #I got how to compute number of parameters in hmm from here:
                #https://discussions.udacity.com/t/verifing-bic-calculation/246165/2
                #and here: https://discussions.udacity.com/t/number-of-parameters-bic-calculation/233235/11
                p = (n_component * n_component) + (2 * n_component * N) - 1
                #Number of parameters = Initial state occupation probabilities +
                #Transition Probabilities + Emission Probabilities
                #p = n_component* n_component + len(candidate_model.means_) + len(candidate_model.covers_)
                logN = np.log(N)
                #computing the BIC value
                bic_value = p*logN - 2*logL
                #since According to BIC, the best model amongst candidates is the
                #model with the lowest BIC score value, we search for
                #the best model by comparing the BIC values so far
                #I found this here: www.stanfordphd.com/BIC.html
                if bic_value < init_score:
                    init_score = bic_value
                    best_n_components = n_component
            except:
                if self.verbose:
                    print("BIC failure on {} with {} states".format(self.this_word, best_n_components))
        #use 3 as default if we fail to find best state from fit
        if best_n_components == 0:
            best_n_components = 3
        #Now create GaussianHMM model with best number of states
        return self.base_model(best_n_components)
        #raise NotImplementedError


class SelectorDIC(ModelSelector):
    ''' select best model based on Discriminative Information Criterion

    Biem, Alain. "A model selection criterion for classification: Application to hmm topology optimization."
    Document Analysis and Recognition, 2003. Proceedings. Seventh International Conference on. IEEE, 2003.
    http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.58.6208&rep=rep1&type=pdf
    DIC = log(P(X(i)) - 1/(M-1)SUM(log(P(X(all but i))
    '''

    def select(self):
        warnings.filterwarnings("ignore", category=DeprecationWarning)
        #TODO implement model selection based on DIC scores
        #Procedure is as follows:
        #Loop from min_n_components to max_n_components
        #fit for each n_component with GaussianHMM(...).fit(...) to get model & logL
        #Loop through all words in sequence since we need to sum over all words
        #except the word we are interested in.
        #Compute DIC value for each model
        #return model with the smallest DIC value
        best_n_components = 0  # best number of states /best n_components
        init_score = float('-inf')  # choose best score to be an arbitrary large number e.g
        for n_component in range(self.min_n_components, self.max_n_components+1):
            #lets compute as follows:
            #DIC = log(P(X(i)) - 1/(M-1)SUM(log(P(X(all but i))
            sumLogP = 0 #Sum of log likelihood
            M = 0  #number of samples  in Sum
            #incase we fail to create candidate model please throw error and pass
            try:
                #candidate model
                candidate_model = self.base_model(n_component)
            except:
                if self.verbose:
                    print("DIC failure on {} with {} states".format(self.this_word, best_n_components))
                pass
            #we create a flag for our word of interest
            flag_word = self.this_word
            for word in self.words:
                if word !=flag_word: #making sure we do not include our word in sum
                    newX, newLength = self.hwords[word] #the current (X,Length) tuple for hmm
                    M += 1
                    try:
                        sumLogP += candidate_model.score(newX, newLength)
                    except:
                        print("DIC SumLogP not computed for word = {}".format(word))
                        pass
            #Now that we have the sum and M for all except our word, lets compute the DIC value
            try:
                logL = candidate_model.score(self.X, self.lengths)
                dic_value = logL - (1/(M-1))*sumLogP
            except:
                print(" Unable to Compute DIC LogL")
                dic_value = 0
            #Now we get the model with the best(largest) DIC value
            #as explained in Biem, Alain's Paper shown above
            if dic_value > init_score:
                init_score = dic_value
                best_n_components = n_component
        #use 3 as default if we fail to find best state from fit
        if best_n_components == 0:
            best_n_components = 3
        #Now create GaussianHMM model with best number of states
        return self.base_model(best_n_components)
        #raise NotImplementedError


class SelectorCV(ModelSelector):
    ''' select best model based on average log Likelihood of cross-validation folds

    '''

    def select(self):
        warnings.filterwarnings("ignore", category=DeprecationWarning)
        # TODO implement model selection using CV
        best_n_components = 0  #best number of states/best n_components
        init_score = float('-inf')  #choose best score to be an arbitrary large number e.g
        #a set of word sequences is broken into three folds using the scikit-learn Kfold class object.
        #n_splits is variable which is helping us to determine
        #what number of splits to find, it is going to be min
        #of 3 and number of samples
        n_splits = min(len(self.sequences), 3)
        for n_component in range(self.min_n_components, self.max_n_components + 1):
            #lets create the HMM model
            try:
                candidate_model = self.base_model(n_component)
                #lets create our kFold object with the number of splits to perform our data
                split_method = KFold(n_splits)
                #to compute the averages
                counter = 0;
                avg_score = 0;
                #Get the indices for train and test setsfor each split
                for cv_train_idx, cv_test_idx in split_method.split(word_sequences):
                    X_train, X_train_length = combine_sequences(cv_train_idx, self.sequences)
                    X_test, X_test_length = combine_sequences(cv_test_idx, self.sequences)
                    #lets train the models on these folds
                    candidate_model = candidate_model.fit(X_train,X_train_length)
                    logL = candidate_model.score(X_test, X_test_length)
                    #update the average score and counter
                    avg_score += logL
                    counter += 1
                #compute the cv_score
                cv_score = avg_score / counter
                #Now select the best state using the cv_score
                #The best state is the state with the highest positive cv score
                if cv_score > init_score:
                    init_score = cv_score
                    best_n_components = n_component
            except:
                if self.verbose:
                    print("CV failure on {} with {} states".format(self.this_word, best_n_components))
                pass
        #Use 3 as default if we fail to find best state from fit
        if best_n_components == 0:
            best_n_components = 3
        #Now create GaussianHMM model with best number of states
        return self.base_model(best_n_components)
        #raise NotImplementedError
