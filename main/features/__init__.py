import os

CQM_CALCULATOR = os.environ.get("CQM_CALCULATOR", "timelapse")  # or "figmd"
VALID_CALCULATORS = ("timelapse", "figmd", "figmd-live")
if CQM_CALCULATOR in VALID_CALCULATORS:
    cqm_calculator = CQM_CALCULATOR
else:
    assert False, "CQM_CALCULATOR is '{calc}', but may only be one of {calcs}".format(
        calc=CQM_CALCULATOR, calcs=", ".join(["'" + s + "'" for s in VALID_CALCULATORS])
    )
