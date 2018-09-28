from snorkel.learning import GenerativeModel

def train_generative_model(data_matrix, burn_in=10, epochs=100, reg_param=1e-6, 
    step_size=0.001, deps=[], lf_propensity=False):
    """
    This function is desgned to train the generative model
    
    data_matrix - the label function matrix which contains the output of all label functions
    burnin - number of burn in iterations
    epochs - number of epochs to train the model
    reg_param - how much regularization is needed for the model
    step_size - how much of the gradient will be used during training
    deps - add dependencey structure if necessary
    lf_propensity - boolean variable to determine if model should model the likelihood of a label function
    
    return a fully trained model
    """
    model = GenerativeModel(lf_propensity=lf_propensity)
    model.train(
        data_matrix, epochs=epochs,
        burn_in=burn_in, reg_param=reg_param, 
        step_size=step_size, reg_type=2
    )
    return model