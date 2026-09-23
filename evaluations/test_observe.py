import os
os.environ["LANGFUSE_PUBLIC_KEY"]="pk-lf-test"
os.environ["LANGFUSE_SECRET_KEY"]="sk-lf-test"
from langfuse import observe, propagate_attributes
@observe()
def test():
    with propagate_attributes(tags=["test"]):
        pass
test()
