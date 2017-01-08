from .relu import ReLu
from .affine import Affine


class ELU(Affine):
    name = 'elu'
    @property
    def describe_params(self):
        '''
        Yields (name, shape, initializer) triples describing the weights directly
        owned by the layer.
        '''
        #def init(W, **kwargs):
        #    W += self.ops.he_normal_init(W.shape, W.shape[-1])
        init = self.ops.xavier_uniform_init
        yield 'W-%s' % self.name, (self.nr_out, self.nr_in), init
        yield 'b-%s' % self.name, (self.nr_out,), None
 
    def predict_batch(self, X):
        output = Affine.predict_batch(self, X)
        self.ops.elu(output, inplace=True)
        return output

    def begin_update(self, input_BI, dropout=0.0):
        output_BO, finish_affine = Affine.begin_update(self, input_BI)
        def finish_update(gradient, *args, **kwargs):
            self.ops.backprop_elu(gradient, output_BO, inplace=True)
            return finish_affine(gradient, *args, **kwargs)
        return output_BO, finish_update


def fwd_elu(ops, x):
    return x * (x > 0) + ((x <= 0) * (ops.xp.exp(x) - 1))


def bwd_elu(ops, x):
    return (x > 0) + (x <= 0) * ops.xp.exp(x)

