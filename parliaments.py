#!/usr/bin/env python3
"""The (lowercase) parliament codes, and available tasks for each
    parliament.
"""

# The populism indices for many parliamnets are currently incomplete
# because of issues of matching party/group codes across different
# datasets.

# Note: for RS and UA, there is a single value for populism. 'populism' is 
# set to false for these parliamaents, but it can still be useful
#  in case people use multi-lingual models.
parl_task = {
        "at":     {'orientation': True, 'power': True, 'populism': True},
        "ba":     {'orientation': True, 'power': True, 'populism': True}, 
        "be":     {'orientation': True, 'power': True, 'populism': True},
        "bg":     {'orientation': True, 'power': True, 'populism': True}, 
        "cz":     {'orientation': True, 'power': True, 'populism': True}, 
        "dk":     {'orientation': True, 'power': True, 'populism': True}, 
        "ee":     {'orientation': True, 'power': False, 'populism': True}, 
        "es-ct":  {'orientation': True, 'power': True, 'populism': False},
        "es-ga":  {'orientation': True, 'power': True, 'populism': False},
        "es-pv":  {'orientation': True, 'power': True, 'populism': False},
        "es":     {'orientation': True, 'power': True, 'populism': True}, 
        "fi":     {'orientation': True, 'power': True, 'populism': True}, 
        "fr":     {'orientation': True, 'power': True, 'populism': True}, 
        "gb":     {'orientation': True, 'power': True, 'populism': True}, 
        "gr":     {'orientation': True, 'power': True, 'populism': True}, 
        "hr":     {'orientation': True, 'power': True, 'populism': True}, 
        "hu":     {'orientation': True, 'power': True, 'populism': True}, 
        "is":     {'orientation': True, 'power': False, 'populism': True}, 
        "it":     {'orientation': True, 'power': True, 'populism': False}, 
        "lv":     {'orientation': True, 'power': True, 'populism': True}, 
        "nl":     {'orientation': True, 'power': True, 'populism': True}, 
        "no":     {'orientation': True, 'power': False, 'populism': True}, 
        "pl":     {'orientation': True, 'power': True, 'populism': True},
        "pt":     {'orientation': True, 'power': True, 'populism': True},
        "rs":     {'orientation': True, 'power': True, 'populism': False},
        "se":     {'orientation': True, 'power': False, 'populism': True},
        "si":     {'orientation': True, 'power': True, 'populism': True},
        "tr":     {'orientation': True, 'power': True, 'populism': True},
        "ua":     {'orientation': True, 'power': True, 'populism': False},
}
