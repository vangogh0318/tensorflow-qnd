import tensorflow as tf
from gargparse import ARGS

from . import flag
from .estimator import def_estimator
from .inputs import def_def_train_input_fn
from .inputs import def_def_eval_input_fn



# TODO: Where to set this? Or, is this the same as Estimator.model_dir?
# add_flag("summary_dir", default="summary", help="Directory containing checkpoint and event files")


def def_def_experiment_fn():
  adder = flag.FlagAdder()

  works_with = lambda name: "Works only with {}".format(name)
  train_help = works_with("qnd.train_and_evaluate()")

  adder.add_flag("train_steps", type=int, help=train_help)
  adder.add_flag("eval_steps", type=int, help=works_with("qnd.evaluate()"))
  adder.add_flag("min_eval_frequency", type=int, default=1, help=train_help)

  estimator = def_estimator()
  def_train_input_fn = def_def_train_input_fn()
  def_eval_input_fn = def_def_eval_input_fn()

  def def_experiment_fn(model_fn, file_reader):
    def experiment_fn(output_dir):
      return tf.contrib.learn.Experiment(
          estimator(model_fn, output_dir),
          def_train_input_fn(file_reader),
          def_eval_input_fn(file_reader),
          **{arg: getattr(ARGS, arg) for arg in adder.flags})

    return experiment_fn

  return def_experiment_fn
