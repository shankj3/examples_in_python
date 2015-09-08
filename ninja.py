"""
Ninja - Fancy variable replacement.

by: Emily Langer
"""

import bisect
import datetime
import json
import logging
import os
import time
import urllib.error
import urllib.request


test_string = 'xx{{a{#b{{c}}{{a}}#}}}xx{{d}}'

DIR = os.path.dirname(os.path.realpath(__file__))
LOGS_DIR = os.path.join(DIR, 'logs')
SERVER_WSGI_PORT = 8707

# logger = logging.getLogger('Glasgow')

# config_parser = configparser.ConfigParser()
# config_parser.read(os.path.join(DIR, 'client', 'pynet_client.ini'))
# config = config_parser['Main']
# HACK: Overriding the config, cause this is all dumb.
config = {'pynet_server_host': 'qatools001.chq.ei'}

# Disable the proxy
proxy_support = urllib.request.ProxyHandler({})
opener = urllib.request.build_opener(proxy_support)
urllib.request.install_opener(opener)


class Replacement(object):
    # start and end are currently superfluous and can probably be removed.
    def __init__(self, start, end, repl_type, old_str, parameter, has_sub_repl=None, new_str=None, resource=None,
                 query=None, dtformat=None):
        self.start = start
        self.end = end
        self.repl_type = repl_type
        self.old_str = old_str
        self.new_str = new_str
        self.parameter = parameter
        self.has_sub_repl = has_sub_repl
        self.resource = resource
        self.query = query
        self.dtformat = dtformat

    def __repr__(self):
        return ('Replacement(start=' + str(self.start) + ', ' +
                'end=' + str(self.end) + ', ' +
                'repl_type=' + str(self.repl_type) + ', ' +
                'old_str=' + str(self.old_str) + ', ' +
                'new_str=' + str(self.new_str) + ', ' +
                'parameter=' + str(self.parameter) + ', ' +
                'has_sub_repl=' + str(self.has_sub_repl) + ', ' +
                'resource=' + str(self.resource) + ', ' +
                'query=' + str(self.query) + ', ' +
                'dtformat=' + str(self.dtformat) + ')'
                )

    def __str__(self):
        return ('Replacement(start=' + str(self.start) + ', ' +
                'end=' + str(self.end) + ', ' +
                'repl_type=' + str(self.repl_type) + ', ' +
                'old_str=' + str(self.old_str) + ', ' +
                'new_str=' + str(self.new_str) + ', ' +
                'parameter=' + str(self.parameter) + ', ' +
                'has_sub_repl=' + str(self.has_sub_repl) + ', ' +
                'resource=' + str(self.resource) + ', ' +
                'query=' + str(self.query) + ', ' +
                'dtformat=' + str(self.dtformat) + ')'
                )

    def __eq__(self, other):
        if (self.start == other.start and
            self.end == other.end and
            self.repl_type == other.repl_type and
            self.old_str == other.old_str and
            self.new_str == other.new_str and
            self.parameter == other.parameter and
            self.has_sub_repl == other.has_sub_repl and
            self.resource == other.resource and
            self.query == other.query and
            self.dtformat == other.dtformat):
            return True
        else:
            return False

    def __ne__(self, other):
        if (self.start == other.start and
            self.end == other.end and
            self.repl_type == other.repl_type and
            self.old_str == other.old_str and
            self.new_str == other.new_str and
            self.parameter == other.parameter and
            self.has_sub_repl == other.has_sub_repl and
            self.resource == other.resource and
            self.query == other.query and
            self.dtformat == other.dtformat):
            return False
        else:
            return True


class VarMap(object):
    def __init__(self, mapped=None, assigned=None, service_name=None, logger_name=None):
        if mapped is None:
            mapped = {}
        if assigned is None:
            assigned = {}
        self.mapped = mapped
        self.assigned = assigned
        self.service_name = service_name

    def get_mapped_vars(self):
        return self.mapped[self.service_name]

    def get_xpaths_to_ignore(self):
        value_string = self.get_mapped_var('xpath_to_ignore')
        if value_string is not None:
            xpaths = value_string.splitlines()
        else:
            xpaths = []

        return xpaths

    def get_mapped_var(self, var):
        return self.mapped[self.service_name].get(var)

    def get_assigned_var(self, var):
        return self.assigned.get(var)

    def set_test_case_id(self, test_case_id):
        self.mapped[self.service_name]['test_case_id'] = test_case_id

    def map_pynet_response(self, response):
        # We iterate over response to handle special things
        # like fen_comp that return multiple values.
        for key in response:
            self.assigned[key] = response[key]
        return self

    def __repr__(self):
        return ('VarMap(mapped=' + str(self.mapped) + ', ' +
                'assigned=' + str(self.assigned) + ', ' +
                'service_name=' + str(self.service_name) + ')'
                )

    def __str__(self):
        return ('VarMap(mapped=' + str(self.mapped) + ', ' +
                'assigned=' + str(self.assigned) + ', ' +
                'service_name=' + str(self.service_name) + ')'
                )


def split_replacement_query(s):
    if '?' in s:
        var, query = s.split('?', maxsplit=1)
    else:
        var, query = s, None
    return var, query


def split_sub_replacement(s):
    if '=' in s:
        new_var, resource = s.split('=', maxsplit=1)
    else:
        # new_var, resource = None, s
        raise Exception('No assignment variable specified. "=" required in assignment replacements.')
    return new_var, resource


def find_replacements(s):
    """This works using the idea that if we have two lists, one of left brackets,
    and one of the corresponding right brackets, that we can figure out how to
    pair them up. We do this by working from the end of the "left-side" list,
    finding the nearest "right-side" bracket, and popping it off the list.
    """
    # Replacements lists will contain lists consisting of [str_index_of_first_replacement_key_character, bracket_type]
    # Why not tuples? No particular reason, I don't think...
    left_replacement_brackets = []
    right_replacement_brackets = []
    markers = {'{': '}',
               '#': '#',
               '%': '%',
               '@': '@',
               '$': '$'}

    repl_types = {'{': 'direct',
                  '#': 'assign',
                  '%': 'pynet',
                  '@': 'seq',
                  '$': 'maths'}

    end = len(s) - 1
    offset = 0  # Used to slice the string as we iterate, so we don't .find() the same (first) bracket each time.
    distance_from_start = 0  # Used to keep track of our position relative to the original string, not the sliced one.

    # Find all instances of left brackets, and figure out the bracket type.
    while distance_from_start < end:
        # Find the first left bracket.
        index = s[offset:].find('{')
        # Calculate its distance from the start
        distance_from_start = index + offset
        # If index != -1, we found a bracket. Make sure it's a legit replacement by verifying
        # that the character after it is a valid marker type. If so, add a Replacement() to the
        # list of found left-side bracket sets.
        if index != -1 and s[distance_from_start + 1] in markers.keys():
            left_replacement_brackets.append([distance_from_start + 2, s[distance_from_start + 1]])
            offset = distance_from_start + 2
        # We didn't find any left brackets in the rest of the string, so we're done.
        elif index == -1:
            break
        # The bracket we found wasn't followed by a valid marker, so it's not a replacement. Advance the index
        # so we don't find the same bracket again. We advance two instead of one, because if we'd found another
        # left bracket, it would have been a valid replacement. Yes, this means we can't have '{{' anywhere in
        # our non-parameterized text.
        else:
            offset = distance_from_start + 2
            continue

    # Reset and prepare to search again
    offset = 0
    distance_from_start = 0

    # It's way easier to do this from the right side...
    reversed_s = s[::-1]

    # Find all instances of right brackets, and figure out the bracket type, pretty much like the above.
    while distance_from_start <= end:
        index = reversed_s[offset:].find('}')
        distance_from_start = index + offset
        if index != -1 and reversed_s[distance_from_start + 1] in markers.values():
            # We still want to find record the index relative to the un-reversed string.
            right_replacement_brackets.append([end - (distance_from_start + 1), reversed_s[distance_from_start + 1]])
        elif index == -1:
            break
        offset = distance_from_start + 2

    # Reverse the lists, (technically, we un-reverse the right) so we can use the
    # handy bisect library.
    reversed_left_brackets = sorted(left_replacement_brackets, reverse=True)
    reversed_right_brackets = sorted(right_replacement_brackets)

    replacements = []
    # Starting with the left_bracket with the highest index...
    for left_bracket in reversed_left_brackets:
        # Unpack the left bracket
        l_index, l_marker = left_bracket
        # Basically we assume that if we take the last left bracket, we should find its matching right bracket
        # by looking for the first right bracket whose index is greater than our left bracket's.
        # bisect.bisect_left is used to "Locate the insertion point for x in a to maintain sorted order".
        # Instead of using it to figure out where to insert our left bracket, we use it to find the index
        # of our matching right bracket, which we pop off the list of right brackets.
        # Remember, our "reversed_right_brackets" are now actually in ascending order by index.
        reversed_r_index = bisect.bisect_left(reversed_right_brackets, left_bracket)
        r_index, r_marker = reversed_right_brackets.pop(reversed_r_index)
        # Quick sanity check to make sure we have the same marker type, then we create our Replacement()
        if markers[l_marker] == r_marker:
            new_replacement = Replacement(start=l_index - 2,
                                          end=r_index + 2,
                                          repl_type=repl_types[l_marker],
                                          old_str=s[l_index - 2:r_index + 2],
                                          parameter=s[l_index:r_index].strip(),
                                          has_sub_repl=None
                                          )
            replacements.append(new_replacement)
        else:
            # To my knowledge, this error has never been logged. Changed to Exception to make sure...
            raise Exception('Uh oh, we have mismatched markers! Something went very wrong')

    # We've already found all of the replacements above, but we need to see for each replacement whether or not
    # it has any sub-replacements. If it does, we'll have to resolve those first when we do replacements later.
    for repl in replacements:
        index = repl.parameter.find('{')
        if index != -1 and repl.parameter[index + 1] in markers.keys():
            repl.has_sub_repl = True
        else:
            repl.has_sub_repl = False

    # A little bit of special casing to prepare replacements to generate values.
    for repl in replacements:
        if repl.repl_type in ['pynet', 'seq'] and repl.has_sub_repl is False:
            repl.resource, repl.query = split_replacement_query(repl.parameter)
            if repl.query and repl.query.startswith('dtformat='):
                repl.dtformat = repl.query[9:]

    return replacements


def apply_replacement(test_str, repl):
    logger = logging.getLogger()
    try:
        if type(repl.old_str) != str or type(repl.new_str) != str:
            logger.error(repl)
        test_str = test_str.replace(repl.old_str, repl.new_str)
        # logger.debug('Replacing: {0} with {1}'.format(repl.old_str, repl.new_str))
    # TODO: This exception is probably not applicable anymore.
    except KeyError:
        logger.error('Could not find requested variable while applying replacements: ' + str(repl.old_str))
        return None
    return test_str


def replace_mapped(test_str, var_map, replacements):
    # repl_types = ['direct', 'assign', 'pynet', 'seq', 'maths']]
    # Replacement(start=24, end=29, repl_type=direct, old_str={{d}}, new_str=None, parameter=d, has_sub_repl=False)
    # Success count is used to see if we should make another pass or not. If nothing changed this pass,
    # (i.e. success_count = 0), then doing another pass isn't going to help.
    success_count = 0
    # If there are sub-replacements within a replacement, it's not ready to be substituted yet.
    # If you need to generate something before you do a mapped lookup, you're Doing It Wrong.
    ready_mapped_repls = [r for r in replacements
                          if r.repl_type in ['direct', 'assign'] and r.has_sub_repl is False]

    for repl in ready_mapped_repls:
        # Easy. Just go get the value from the varmap.
        if repl.repl_type == 'direct':
            repl.new_str = var_map.get_mapped_var(repl.parameter)
            if repl.new_str is not None:  # if it's None, the parameter couldn't be found in the varmap.
                success_count += 1
        elif repl.repl_type == 'assign':
            # Separate the variable we're assigning to from the value we want to assign to it.  The value may
            # itself be another replacement! That's okay. We'll drop it in place, and catch it next pass.
            new_var, value = split_sub_replacement(repl.parameter)
            repl.new_str = value
            # Check to make sure we aren't double-mapping... If not, go ahead and assign the new_str (i.e. the value)
            # to the key in the varmap. If the value is another replacement, it'll get referenced at some point
            # by a direct replacement, and resolved on the pass after that happens. It's confusing, but it works.
            if var_map.get_mapped_var(new_var) is None:
                var_map.assigned[new_var] = repl.new_str
            else:
                raise Exception('Tried to assign var to mapped var! {0}'.format(repl.parameter))
        # Finally, if we were able to find a replacement string, make the replacement. If not, it's likely
        # this replacement is referencing something that hasn't been generated/assigned yet.
        if repl.new_str is not None:
            test_str = apply_replacement(test_str, repl)

    return test_str, success_count


def resolve_generated(strings, var_map):
    grouped_replacements = []
    for string in strings:
        grouped_replacements.extend(find_replacements(string))

    # If there are sub-replacements within a replacement, it's not ready to be substituted yet.
    ready_generated_repls = [r for r in grouped_replacements
                             if r.repl_type in ['pynet', 'seq'] and
                             r.has_sub_repl is False]

    # TODO: Maybe validate resources so we don't blow up the service? Or just let it fail and catch it... hmmm.
    unique_local_resources = []
    unique_remote_resources = []
    # Identify the unique datetime resources for each generator type. We need to de-dupe these particular ones
    # so we only make one request for each resource, so they're consistent within the same request/response.
    for repl in ready_generated_repls:
        if repl.repl_type == 'pynet' and repl.resource.startswith(('d', 'm', 'y')):
            if repl.resource not in unique_local_resources:
                unique_local_resources.append(repl.resource)
        if repl.repl_type == 'pynet' and repl.resource.startswith(('fen', 'legacy')):
            if 'fencomp' not in unique_local_resources:
                unique_local_resources.append('fencomp')

        if repl.repl_type == 'seq' and repl.resource.startswith(('d', 'm', 'y')):
            if repl.resource not in unique_remote_resources:
                unique_remote_resources.append(repl.resource)
        if repl.repl_type == 'seq' and repl.resource.startswith(('fen', 'legacy')):
            if 'fencomp' not in unique_remote_resources:
                unique_remote_resources.append('fencomp')

    # Go get the values for  each unique resource and map them into the var map.
    # Limitation: don't manually assign to any var names that have PYNET counterparts, because the resource/value
    # pairs get mapped into the varmap just like any other assignment would.
    for resource in unique_local_resources:
        var_map.map_pynet_response(get_local_generated_var(resource))
    for resource in unique_remote_resources:
        var_map.map_pynet_response(get_remote_generated_var(resource))

    # Other resources that might not be the same each time (e.g. sequential, hsNumber, etc.)
    # but need to be the same within the test case should be assigned to a variable,
    # then the variable should be referenced in subsequent replacements within the case.
    for repl in ready_generated_repls:
        if repl.repl_type == 'pynet' and not repl.resource.startswith(('d', 'm', 'y', 'fen', 'legacy')):
            var_map.map_pynet_response(get_local_generated_var(repl.resource, repl.query))
        elif repl.repl_type == 'seq' and not repl.resource.startswith(('d', 'm', 'y', 'fen', 'legacy')):
            var_map.map_pynet_response(get_remote_generated_var(repl.resource, repl.query))

    for index, string in enumerate(strings):
        replacements = find_replacements(string)
        ready_to_replace = [r for r in replacements
                             if r.repl_type in ['pynet', 'seq'] and
                             r.has_sub_repl is False]

        # Update the replacements' new_str with the now-ready text.
        for repl in ready_to_replace:
            # Datetime and other resource types are handled differently. Datetimes might need formatting...
            if repl.dtformat:
                repl.new_str = format_datetime(var_map.assigned[repl.resource], repl.dtformat)
            else:
                repl.new_str = var_map.assigned[repl.resource]
            # Finally, apply the replacements to the strings
            string = apply_replacement(string, repl)
            strings[index] = string

    return strings, var_map


def resolve_assigned(test_str, var_map, replacements):
    # repl_types = ['direct', 'assign', 'pynet', 'seq']
    # Replacement(start=24, end=29, repl_type=direct, old_str={{d}}, new_str=None, parameter=d, has_sub_repl=False)
    logger = logging.getLogger()
    # There shouldn't be any 'pynet' or 'seq tests left.
    direct_repls = [r for r in replacements
                    if r.repl_type == 'direct' and
                    r.has_sub_repl is False]

    assign_repls = [r for r in replacements
                    if r.repl_type == 'assign' and
                    r.has_sub_repl is False]

    maths_repls = [r for r in replacements
                   if r.repl_type == 'maths' and
                   r.has_sub_repl is False]

    # TODO: De-dupe this code from replace_mapped() :/ See there for more comments.
    for repl in assign_repls:
        new_var, value = split_sub_replacement(repl.parameter)
        repl.new_str = value
        if var_map.get_mapped_var(new_var) is None:
            var_map.assigned[new_var] = repl.new_str
        else:
            logger.error('Tried to assign var to mapped var! {0}'.format(repl.parameter))
        if repl.new_str is not None:
            test_str = apply_replacement(test_str, repl)

    for repl in maths_repls:
        repl.new_str = str(eval(repl.parameter))
        if repl.new_str is not None:
            test_str = apply_replacement(test_str, repl)

    # This time we're counting failures instead of successes, because we know if our fail count
    # is equal to the number of remaining replacements, then subsequent passes aren't going to help
    # reduce the number of failures, because, well... they won't do anything.
    failed_resolve_count = 0
    for repl in direct_repls:
        repl.new_str = var_map.get_assigned_var(repl.parameter)
        if repl.new_str is None:
            failed_resolve_count += 1
        else:
            test_str = apply_replacement(test_str, repl)

    return test_str, var_map, failed_resolve_count


def get_local_generated_var(resource, query=None):
    import pncommon.pnwsgi as pnwsgi
    logger = logging.getLogger()
    response_json = pnwsgi.local_get_vars(resource, query)
    # TODO: I think this might blow up if the resource is bad....
    try:
        response = json.loads(response_json)
    except ValueError as e:
        logger.info(e)
        logger.info('Bad PYNET response! Check your defined resources. {0}?{1}'.format(resource, query))
        raise e
    return response


def get_remote_generated_var(resource, query=None):
    logger = logging.getLogger()
    py_time_start = time.time()
    response = None

    try:
        if query is None:
            target = ''.join(('http://', config['pynet_server_host'], ':',
                              str(SERVER_WSGI_PORT), '/pynet-service/v1/get_vars/', resource))
        else:
            target = ''.join(('http://', config['pynet_server_host'], ':',
                              str(SERVER_WSGI_PORT), '/pynet-service/v1/get_vars/',
                              resource, '?', query))
        opened_url = urllib.request.urlopen(target)
        response_json = opened_url.read().decode()
        opened_url.close()
        # TODO: I think this might blow up if the resource is bad....
        response = json.loads(response_json)
    except urllib.error.HTTPError:
        logger.critical('Probably can\'t reach the PYNET server...')
        logger.critical('http://' + config['pynet_server_host'] + ':' +
                        str(SERVER_WSGI_PORT) + '/get_vars/' + resource + ' Query: ' + str(query))
    except Exception as e:
        logger.critical('Could not reach PYNET server! Failing test...')
        raise e
    py_time_end = time.time()
    logger.debug('PYNET server call time: ' + str(py_time_end - py_time_start))
    return response


def format_datetime(datetime_string, frmt):
    default_format = '%Y-%m-%dT%H:%M:%S.%f'
    dt = datetime.datetime.strptime(datetime_string, default_format)
    milliseconds = str(dt.microsecond)[:-3]
    frmt = frmt.replace('%s', milliseconds)
    formatted_dt = dt.strftime(frmt)
    return formatted_dt


def do_the_substitution(var_map, strings):
    """Takes strings and a varmap, finds and applies replacements in the strings.
    Returns updated strings and varmap, and a list of status messages, if any
    from the replacement process (i.e. if something failed, why, etc.)

    It's word behavior.
    It's substitution, baby.
    """
    # Loop count is just here to make sure nobody did anything
    # extraordinarily stupid. Loop will abort if loop count gets
    # too high (i.e. if someone nested replacements too deeply).
    # TODO: Should probably config-ify this. Maybe.
    max_repl_loop_count = 20
    failed_count = 0
    replacements = []
    # We start with mapped vars to pull out any mapped PYNET stuff.
    # Replacements in this loop don't need to be aggregated from the string batch.
    for index, string in enumerate(strings):
        for _ in range(max_repl_loop_count):
            # We break if success_count == 0, that is, we've gone through an
            # iteration without doing any replacements.
            replacements = find_replacements(string)
            string, success_count = replace_mapped(string, var_map, replacements)
            strings[index] = string
            if success_count == 0:
                break
        else:
            raise Exception('Your mapped replacements are way too complex. Or broken.')

    # We've gotten as much as we can from the mapper, and PYNET vars should not be self-referential,
    # and by that I mean generating a variable to construct a reference to another generated variable
    # is a Bad Idea, so we don't support that.
    strings, var_map = resolve_generated(strings, var_map)

    # There should only be replacements that reference assigned variables left, so we handle those next.
    # We can assume that if the last find_replacements was empty, there aren't any more to do here either.
    for index, string in enumerate(strings):
        for _ in range(max_repl_loop_count):
            replacements = find_replacements(string)
            if failed_count < len(replacements):
                string, var_map, failed_count = resolve_assigned(string, var_map, replacements)
                strings[index] = string
            else:
                break
        else:
            raise Exception('Your assignment replacements are way too complex. Or broken.')

    for string in strings:
        # If test_case.string is None here, something has gone wrong above. This is our
        # (probably bad) way of bubbling it up. I think all of those are removed though, so we shouldn't hit this.
        if string is None:
            raise Exception('Something went wrong when building the test case string. Now it\'s empty.')
        else:
            # A final test to make sure nothing got missed. If it did, we're in big trouble.
            replacements = find_replacements(string)
            if replacements:
                raise Exception('There are leftover replacements. Maybe your variable is undefined? '
                                'Check the old_str attribute for each replacement below. \n'
                                '{0}'.format(str(replacements)))
    return strings

