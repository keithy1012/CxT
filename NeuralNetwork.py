import numpy as np

class NeuralNetwork:
    def __init__(self, learning_rate):
        self.learning_rate = learning_rate
        # Use however many input variables we have (10)
        self.weights = np.array([np.random.randn(), np.random.randn(), np.random.randn(), np.random.randn(), np.random.randn(), np.random.randn(), np.random.randn(), np.random.randn(), 
        np.random.randn()])
        self.bias = np.random.randn()
    
    def _sigmoid(self, x):
        return 1 /  (1+np.exp(-x))

    def _sigmoid_deriv(self, x):
        return self._sigmoid(x) * (1-self._sigmoid(x))

    def predict(self, input_vector):
        layer1 = np.dot(input_vector, self.weights) + self.bias
        layer2 = self._sigmoid(layer1)
        prediction = layer2
        return prediction
    
    def _compute_gradients(self, input_vector, target):
        layer1 = np.dot(input_vector, self.weights) + self.bias
        layer2 = self._sigmoid(layer1)
        prediction = layer2;

        derror_dprediction = 2 * (prediction - target)
        deprediction_dlayer1 = self._sigmoid_deriv(layer1)
        dlayer1_dbias = 1
        dlayer1_dweights = (0 * self.weights) + (1*input_vector)

        derror_dbias = (derror_dprediction * deprediction_dlayer1 * dlayer1_dbias)
        derror_dweights = (derror_dprediction * deprediction_dlayer1 * dlayer1_dweights)
    
        return derror_dbias, derror_dweights

    def _update_parameters(self, derror_dbias, derror_dweights):
        self.bias = self.bias - (derror_dbias * self.learning_rate)
        self.weights = self.weights - (derror_dweights * self.learning_rate)

    def train(self, input_vectors, targets, iterations):
        total_errors = []
        for current_iteration in range(iterations):
            random_data_index = np.random.randint(len(input_vectors))
            input_vector = input_vectors[random_data_index]
            target = targets[random_data_index]
            derror_dbias, derror_dweights = self._compute_gradients(input_vector, target)

            self._update_parameters(derror_dbias, derror_dweights)

            if current_iteration % 100 == 0:
                cumulative_error = 0
                for data_instance_index in range(len(input_vectors)):
                    data_point = input_vectors[data_instance_index]
                    target = targets[data_instance_index]

                    prediction = self.predict(data_point)
                    error = np.square(prediction-target)
                    cumulative_error = cumulative_error + error
                total_errors.append(cumulative_error)
        return total_errors