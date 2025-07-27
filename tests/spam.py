from flexfail import ErrorCollector, ErrorCollectorStrategy
from flexfail.exceptions import FlexFailException, FailFastException

########## TEST ########################################################################################################
# Let's assume, negative values are impossible to process, as the values are checkouts, for instance.
checkouts = [10, 20, -30, -40, 50]


def process_check(amount: float):
    if amount < 0:
        raise FlexFailException(data={'description': 'Checkout amount was below zero!', 'amount': amount})
    print(f'Check with amount {amount}$ was successfully processed!')


def process_all(strategy: FailFastException):
    error_collector = ErrorCollector(process_check, strategy)
    try:
        for _ in checkouts:
            error_collector.call(_)
    except FailFastException:
        pass
    print(f'Collected errors:')
    print('\n'.join([str(_.data) for _ in error_collector.errors]))

########## STRATEGY: SKIP ##############################################################################################
print('#################### Strategy: `skip` (just skipping unprocessable data)')
process_all(ErrorCollectorStrategy.skip)

########## STRATEGY: FAIL FAST #########################################################################################
print('#################### Strategy: `fail_fast` (abort if at least one error occurs)')
process_all(ErrorCollectorStrategy.fail_fast)

########## STRATEGY: TRY ALL ###########################################################################################
print('#################### Strategy: `try_all` (try to process all the data and, therefore, collect all the errors)')
process_all(ErrorCollectorStrategy.try_all)