# Author @feliperyan 2021-06-02

# Code adapted to ORTools (https://developers.google.com/optimization) 
# based on example at https://towardsdatascience.com/how-to-develop-optimization-models-in-python-1a03ef72f5b4

# A bakery makes cakes and pies every day of a month. 
# There is: 1 oven, 2 bakers, 1 packaging packer that works only 22 days of the month. 
# The cake requires to use the oven for 1 day and the pie requires 0.5 day. 
# Each baker needs to work for cake 0.5 days and pie 2 days. 
# Packer needs to work for cake 1 day and pie 0.5 days. 
# The profit on each cake is $15 and the profit on each pie is $12. 
# How many should be made to maximize the profit under given conditions?

from typing import Dict

from ortools.linear_solver import pywraplp
solver: pywraplp.Solver = pywraplp.Solver.CreateSolver('SCIP')

# mostly for ease of testing:
def inputs(periodInDays: float, numOfBakers: float, packerWorkingDays: float, 
        priceOfCake: float, priceOfPie: float, numOfPackers: float, bakerEffortForCake: float, 
        bakerEffortForPie: float, bakeTimeCake: float, bakeTimePie: float, numOfOvens: float, packerEffortForCake:float, packerEffortForPie: float):
   
    return {
        'periodInDays': periodInDays,
        'periodInDays': periodInDays,
        'packerWorkingDays': packerWorkingDays,
        'priceOfCake': priceOfCake,
        'priceOfPie': priceOfPie,
        'numOfPackers': numOfPackers,
        'bakerEffortForCake': bakerEffortForCake,
        'bakerEffortForPie': bakerEffortForPie,
        'bakeTimeCake': bakeTimeCake,
        'bakeTimePie': bakeTimePie,
        'numOfOvens': numOfOvens,
        'packerEffortForCake': packerEffortForCake,
        'packerEffortForPie': packerEffortForPie
    }


def runExample(inputs: Dict) -> Dict[str, float]:
    
    infinity = solver.infinity()
    # x and y are integer non-negative variables.
    c = solver.IntVar(0.0, infinity, 'c')
    p = solver.IntVar(0.0, infinity, 'p')

    # The cake requires to use the oven for 1 day and the pie requires 0.5 day
    solver.Add(inputs['bakeTimeCake'] * c + inputs['bakeTimePie'] * p <= inputs['periodInDays'] * inputs['numOfOvens'])
    
    # Each baker needs to work for cake 0.5 days and pie 2 days. 2 bakers.
    solver.Add(inputs['bakerEffortForCake'] * c + inputs['bakerEffortForPie'] * p <= inputs['periodInDays'] * inputs['numOfBakers'])

    # Packer needs to work for cake 1 day and pie 0.5 days. Works 22 days of the month.
    solver.Add(inputs['packerEffortForCake'] * c + inputs['packerEffortForPie'] * p <= inputs['packerWorkingDays'] * inputs['numOfPackers']) 

    solver.Maximize(inputs['priceOfCake'] * c + inputs['priceOfPie'] * p)

    print('Optimising...')
    status = solver.Solve()

    if status == pywraplp.Solver.OPTIMAL:
        print('Solution:')
        print('Maximum Profit =', solver.Objective().Value())
        print('cakes =', c.solution_value())
        print('pies =', p.solution_value())
        return {'max_profit':solver.Objective().Value(), 'cakes': c.solution_value(), 'pies': p.solution_value()}
    else:
        print('The problem does not have an optimal solution.')
        return {}
