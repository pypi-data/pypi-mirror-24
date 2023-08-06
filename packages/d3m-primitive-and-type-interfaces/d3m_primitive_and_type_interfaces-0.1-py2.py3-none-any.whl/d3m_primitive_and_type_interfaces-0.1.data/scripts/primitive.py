import abc

class Primitive():
    def __init__(self):
        """Initializes a primitive.
        """

    @abc.abstractmethod
    def get_type_params():
        """Returns class, representing type of parameters"""

    @abc.abstractmethod
    def get_type_input():
        """Returns class, representing type of input"""

    @abc.abstractmethod
    def get_type_output():
        """Returns class, representing type of output"""

    ######### SUPERVISED LEARNING #########
    # Supports
    # - gradient-based, compositional end-to-end training
    # - gradient-based pre-training
    # - multi-task adaptation
    #######################################

    @abc.abstractmethod
    def set_supervision(self, inputs, outputs):
        """Set inputs and outputs to this primitive.
        """

    @abc.abstractmethod
    def pretrain(self):
        """Fits regressor using supervision.
        """

    @abc.abstractmethod
    def get_params(self):
        """Returns parameter of this primitive.
        """

    @abc.abstractmethod
    def set_params(self):
        """Sets parameter of this primitive.
        """

    @abc.abstractmethod
    def get_params_prior(self):
        """Returns prior primitive for the parameters.
        """

    @abc.abstractmethod
    def set_params_prior(self, primitive):
        """Sets prior primitive for the parameters.
        """

    @abc.abstractmethod
    def log_likelihood(self, input, output):
        """Returns log probability of output under this primitive.

        log p(output | input, params)
        """

    @abc.abstractmethod
    def sample(self, input, num_samples=1):
        """Returns a weighted sample (unnormalized)
        """

    @abc.abstractmethod
    def grad_log_likelihood(self, output):
        """Returns gradient of log p(output | input, params) with respect to
        output.
        """

    @abc.abstractmethod
    def get_score(self, output):
        """Returns gradient of log p(output | input, params) with respect to
        params.
        """

    @abc.abstractmethod
    def set_pretrain_inverse_temperature(self, power):
        """All posterior calcuations are raised to this power in all
        computations

        (prod_i p(output_i | input_i, params))^power
        """

    ######### UNSUPERVISED LEARNING #########
    #
    #########################################

    @abc.abstractmethod
    def log_likelihood(self):
        """
        """
