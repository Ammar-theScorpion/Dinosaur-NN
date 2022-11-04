import random
import numpy as np
import scipy.special


class Nnet:
    def __init__(self, n_input, n_hidden, n_output) -> None:
        self.n_input = n_input
        self.n_output = n_output
        self.n_hidden = n_hidden

        self.w_i_h = np.random.uniform(-0.5, 0.5, size=(self.n_input, self.n_hidden))
        self.w_h_o = np.random.uniform(-0.5, 0.5, size=(self.n_hidden, self.n_output))

        self.activaion_function = lambda x: scipy.special.expit(x)

    def get_output(self, inputList):
        input = np.array(inputList, ndmin=2).T
        input_hiddent = np.dot(self.w_i_h, input)
        output_hidden = self.activaion_function(input_hiddent)
        input_final = np.dot(self.w_h_o, output_hidden)
        output_final = self.activaion_function(input_final)
        return output_final

    def get_max_output(self, input):
        return np.max(self.get_output(input))


    def modify_weights(self):
        Nnet.modify_array(self.w_i_h)
        Nnet.modify_array(self.w_h_o)

    def create_mixed_weights(self, net1, net2):
        self.w_i_h = Nnet.get_mix_from_arrays(net1.w_i_h, net2.w_i_h)
        self.w_h_o = Nnet.get_mix_from_arrays(net1.w_h_o, net2.w_h_o)

    def modify_array(a):
        for x in np.nditer(a, op_flags=['readwrite']):
            if random.random() < 0.2:
                x[...] = np.random.random_sample() - 0.5
        
    
    def get_mix_from_arrays(arr1, arr2):

        total_entries = arr1.size
        num_rows = arr1.shape[0]
        num_cols = arr1.shape[1]

        num_take = total_entries - int(total_entries*0.5)

        idx = np.random.choice(np.arange(total_entries), num_take, replace = False)

        res = np.random.rand(num_rows, num_cols)

        for row in range(num_rows):
            for col in range(num_cols):
                index = row * num_cols + col    
                if index in idx:
                    res[row][col] = arr1[row][col]
                else:
                    res[row][col] = arr2[row][col]
        return res