## Installation
To run the AI locally, follow these steps:
1.  Clone the repo  
    ```sh
    git clone https://github.com/tokudayo/AIFA.git
    ```
2. Setup Python environment
    ```sh
    pip install -r ai/requirements.txt
    ```

## Usage
For evaluation, use either ```eval.py``` or ```webcam.py```. Here is an example of using ``eval.py`` to evaluate:
```sh
python -m scripts.eval
```

## Customizing
The scripts are located in the ```scripts``` folder. You can customize the scripts to fit your needs. 

For example, you can change the evaluator a different exercise:
```python
class AIFlow(object):
    def __init__(self):
        # Change the exercise to evaluate
        self.evaluator = ShoulderPress()
```
