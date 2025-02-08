# PHASE A - STEP 4
# Create *.GEN: Using the downloaded SSURGO data, create default *.GEN files for major components of each Map Unit

# ==========================================
# Requirements:
# a. Calculate lower limit of water content
#   - convert PWP and FC to decimal
#   - In template.gen file, on line 27, replace the value by the formula: PWP + 0.25 (FC-PWP) --> this formula became (PWP + 0.25 (FC-PWP))/100 as of 10/12/2023
#
# b. Update depth to restrictive layer, "depth restrictive" (cm) (resdept_r)
#   - Must extract resdept_r from soildb (corestrictions.xlsx)
#   - replace missing value by 200
#   - In template.gen file, on line 20, the first number:
#       - Whenever resdept_r > 200 cm (a default number for missing values), use a depth to restrictive layer of 305 cm
#
# c. The saturated hydraulic conductivity and layer depth
#   - Extract hzdepb_r and ksat_r from chorizons.xlsx (ksat_r is in um/s)
#   - convert ksat_r from um/s to cm/day
#   - after unit conversion, multiply ksat_r by two
#   - Update hzdepb_r and ksat_r in lines 21-22 in template.gen
#
#
# d. Update Volumetric water content at saturation of the top layer (decimal) (wsatiated_r)
#   - Extract wsatiated_r from chorizons.xlsx
#   - Convert wsatiated_r to decimal
#   - Update wsatiated_r in lines 85, second value in template.gen
#
# e. Update Depth to restrictive layer (cm) (resdept_r)
#   - Extract resdept_r from corestrictions.xlsx
#   - Update resdept_r in lines 80, first value in template.gen
#
# f. Volumetric water content at saturation of the top layer (decimal) (wsatiated_r) will be used to determine the
#    highlighted text below from a table. See OneNote page  "Soil Thermal Conductivity Table" for table.
#   -
#   -
# ==========================================
import os
import pandas as pd
from cigsatbuf_utils.envs import GEN_FILE

# from retrieve_soil_components import extract_soil_inputs_from_tables
MISSING_VALUE_SUB = 200


# Step 2: Do the unit conversions
def convert_to(column, df_oi, unit='decimal'):
    """
    :param unit: 'decimal', 'cm_day', 'cm_hour'
    :param column:
    :param df_oi: df_major_components
    :return: df_major_components with converted columns applied
    """
    from_sec_to_day = 1 / 86400  # there are 86400 seconds in a day
    from_sec_to_hour = 1 / 3600  # there are 3600 seconds in an hour
    from_um_to_cm = 1e-4
    from_um_per_sec_to_cm_per_day = from_um_to_cm / from_sec_to_day
    from_um_per_sec_to_cm_per_hour = from_um_to_cm / from_sec_to_hour
    factors = {'decimal': 0.01, 'cm_day': from_um_per_sec_to_cm_per_day, 'cm_hour': from_um_per_sec_to_cm_per_hour}

    df_oi[column] = df_oi[column] * factors[unit]

    return df_oi


def convert_ksat(df):
    df = convert_to('ksat_r', df, unit='cm_hour')
    df['ksat_r'] = 2 * df['ksat_r']
    return df


NUM_MAX_NLAYERS = 5


# Step 4: Calculate lower limit of water content: PWP + 0.25 (FC-PWP) = 0.75PWP + 0.25FC --> this formula became (PWP + 0.25 (FC-PWP))/100 as of 10/12/2023
def calc_low_limit_water_content(df_oi):
    # Volumetric PWP = wfifteenbar_r
    # Volumetric FC  = wthirdbar_r
    return 0.75 * df_oi['wfifteenbar_r'] + 0.25 * df_oi['wthirdbar_r']


def create_map_ll_water_content(df, multi_df_param_):
    map_llwc = dict()
    multi_df_param = multi_df_param_

    def cal_llwc(mukey, cokey, multi_df_param=multi_df_param):
        multi_df_oi = multi_df_param.loc[mukey].loc[cokey]
        layers_list = multi_df_oi.index.values.tolist()
        pwp_list = multi_df_oi['wfifteenbar_r'].values.tolist()
        fc_list = multi_df_oi['wthirdbar_r'].values.tolist()
        layer_mapped_to_ = {l: [pwp_list[i], fc_list[i]] for i, l in enumerate(layers_list)}
        top_layer = min(layer_mapped_to_.keys())
        pwp_fc = layer_mapped_to_[top_layer]
        # llwc = 0.75 * pwp_fc[0] + 0.25 * pwp_fc[1]
        pwp, fc = layer_mapped_to_[top_layer]
        llwc = (pwp + 0.25 * (fc-pwp))/100
        return llwc

    mukey_list = df['mukey'].to_list()
    cokey_list = df['cokey'].to_list()

    for m, c in zip(mukey_list, cokey_list):
        k = str(m) + '_' + str(c)
        map_llwc[k] = cal_llwc(m, c)

    return map_llwc


def create_map_wsatiated(df, multi_df_param_):
    map_sat = dict()
    multi_df_param = multi_df_param_

    def cal_llwc(mukey, cokey, multi_df_param=multi_df_param):
        multi_df_oi = multi_df_param.loc[mukey].loc[cokey]
        layer_mapped_to_wsat_dict = multi_df_oi['wsatiated_r'].to_dict()
        top_layer = min(layer_mapped_to_wsat_dict.keys())
        return layer_mapped_to_wsat_dict[top_layer]

    mukey_list = df['mukey'].to_list()
    cokey_list = df['cokey'].to_list()

    for m, c in zip(mukey_list, cokey_list):
        k = str(m) + '_' + str(c)
        map_sat[k] = cal_llwc(m, c)

    return map_sat


def create_map_titles(df, multi_df_param_):
    map_tiles = dict()
    multi_df_param = multi_df_param_

    def get_title(mukey, cokey, muname, multi_df_param=multi_df_param):
        multi_df_oi = multi_df_param.loc[mukey].loc[cokey]
        # layers = multi_df_oi.loc[mukey].loc[cokey].index.get_level_values(0)
        layers_list = multi_df_oi.index.values.tolist()
        num_of_layers = len(layers_list)
        title = f"{num_of_layers} layers - Mukey: {mukey} - Cokey: {cokey} - {muname}\n"
        return title

    mukey_list = df['mukey'].to_list()
    cokey_list = df['cokey'].to_list()
    muname_list = df['muname'].to_list()

    for m, c, name in zip(mukey_list, cokey_list, muname_list):
        k = str(m) + '_' + str(c)
        map_tiles[k] = get_title(m, c, name)

    return map_tiles


def get_line_27_gen(mukey, cokey, map_llwc):
    k = str(mukey) + '_' + str(cokey)
    ll_water_content = map_llwc[k]
    val = round(ll_water_content, 3)
    updated_line = 6 * ' ' + str(val)[1:] + "\n"
    return updated_line


def get_line_21_gen(mukey, cokey, multi_df_param):
    """
    This function creates a line that match the requirement of task A3c.
    :param mukey:
    :param cokey:
    :param multi_df_param: a df with a multiindex (['mukey', 'cokey', 'hzdepb_r']) values
    :return: a string ( a formatted line)
    """
    multi_df_oi = multi_df_param.loc[mukey].loc[cokey]
    layers_list = multi_df_oi.index.values.tolist()
    ksat_list = multi_df_oi['ksat_r'].values.tolist()
    # layer_mapped_to_ksat_dict = multi_df_oi['ksat_r'].to_dict()
    layer_mapped_to_ksat_tuples = zip(layers_list, ksat_list)

    line_21 = ""
    for layer, ksat in layer_mapped_to_ksat_tuples:
        # line_21 += format(layer, '-4n') + '.' + format(ksat, ' 5.2f')    # in the template, looks like ksat should be 5 chars long
        # line_21 += format(layer, '-4n') + '.' + format(ksat, '5.2f')  # but there arevalues of ksat that are > 5 chars long
        kval = format(ksat, '5.1f') if len(format(ksat, '5.2f')) > 5 else format(ksat, '5.2f')
        line_21 += f"{format(layer, '-3n')}.0{kval}"
    # Apparently there ought to be NUM_MAX_NLAYERS, so append these values if some are missing
    for i in range(NUM_MAX_NLAYERS - len(layers_list)):
        line_21 += "   0.  .00"

    line_21 += "\n"
    return line_21


def get_line_85_gen(mukey, cokey, map_wsatiated):
    k = str(mukey) + '_' + str(cokey)
    wsat = map_wsatiated[k]
    val = round(wsat, 3)
    updated_line = "  0.00    " + format(val, '-5.3f') + "\n"
    return updated_line


def get_job_title(mukey, cokey, map_titles):
    k = str(mukey) + '_' + str(cokey)
    title = map_titles[k]
    return title


def get_gen_output_name(mukey, cokey, out_dir):
    if not os.path.exists(out_dir):
        os.mkdir(out_dir)
    name = str(mukey) + '_' + str(cokey)
    out_file = out_dir / name / f"{name}_stepB.gen"
    return out_file


def update_gen(gen_file, df_row, multi_df, map_llwc, map_wsatiated, map_titles, gen_file_template=GEN_FILE):
    with open(gen_file_template, 'r') as template_file:
        template_lines = template_file.readlines()

        with open(gen_file, 'w') as this_gen:
            for line_num, sentence in enumerate(template_lines, 1):

                if line_num == 2:
                    updated_line = get_job_title(df_row['mukey'], df_row['cokey'], map_titles)

                elif line_num == 3:
                    updated_line = '\n'

                # b. In template.gen file, on line 20, the first number with resdept_r:
                elif line_num == 20:
                    val = df_row['resdept_r']
                    val = 305 if val > 200 else val
                    updated_line = 4 * ' ' + format(val, '.2f') + "      0.70\n"

                # c. The saturated hydraulic conductivity and layer depth
                elif line_num == 21:
                    updated_line = get_line_21_gen(df_row['mukey'], df_row['cokey'], multi_df)

                # a. In template.gen file, on line 27, replace the value by ll_water_content
                elif line_num == 27:
                    # val = round(df_row['ll_water_content'], 3)
                    # updated_line = 6 * ' ' + str(val)[1:] + "\n"
                    updated_line = get_line_27_gen(df_row['mukey'], df_row['cokey'], map_llwc)

                # e. Update Depth to restrictive layer (cm) (resdept_r)
                elif line_num == 80:
                    val = df_row['resdept_r']
                    val = 305 if val > 200 else val
                    updated_line = format(val, '.2f') + "   10.00\n"

                # d. Update Volumetric water content at saturation of the top layer (decimal) (wsatiated_r)
                elif line_num == 85:
                    # val = df_row['wsatiated_r']
                    # # updated_line = format(val, '-6.2f') + "    0.400\n"
                    # updated_line = "  0.00    " + format(val, '-5.3f') + "\n"
                    updated_line = get_line_85_gen(df_row['mukey'], df_row['cokey'], map_wsatiated)

                else:
                    updated_line = sentence

                updated_line = updated_line
                this_gen.writelines(updated_line)


def make_gen_file(relevant_soil_info_fpath, gen_fpath, gen_file_template=None):

    if gen_file_template is None:
        gen_file_template = GEN_FILE

    def concatenate_unique(series):
        unique_values = series.dropna().unique()
        return ', '.join(unique_values)

    agg_funcs = {
        'sandtotal_r': 'mean',
        'silttotal_r': 'mean',
        'claytotal_r': 'mean',
        'dbthirdbar_r': 'mean',
        'wthirdbar_r': 'mean',
        'wfifteenbar_r': 'mean',
        'hzdepb_r': 'mean',
        'muname': concatenate_unique,
        'ksat_r': 'mean',
        'resdept_r': 'mean',
        'wsatiated_r': 'mean'
    }

    # Step 1: extract all the soil components needed for this task:
    # 'wfifteenbar_r', 'wthirdbar_r', 'resdept_r', 'hzdepb_r', 'ksat_r', 'wsatiated_r',
    df_major_components_oi = pd.read_excel(relevant_soil_info_fpath)
    df_major_components_oi.columns = ['sandtotal_r', 'silttotal_r', 'claytotal_r', 'dbthirdbar_r', 'wthirdbar_r',
                                      'wfifteenbar_r', 'mukey', 'cokey', 'hzdepb_r', 'muname', 'ksat_r', 'resdept_r',
                                      'wsatiated_r']


    # convert wthirdbar_r, wfifteenbar_r, wsatiated_r to decimal
    df_major_components_oi = convert_to('wthirdbar_r', df_major_components_oi, unit='decimal')
    df_major_components_oi = convert_to('wfifteenbar_r', df_major_components_oi, unit='decimal')
    df_major_components_oi = convert_to('wsatiated_r', df_major_components_oi, unit='decimal')

    df_major_components_oi = convert_ksat(df_major_components_oi)

    # Step 3: for the column 'resdept_r', replace missing values with 200
    df_major_components_oi['resdept_r'] = df_major_components_oi['resdept_r'].fillna(MISSING_VALUE_SUB)

    # Step #: create a multi-index df
    values_column = ['sandtotal_r', 'silttotal_r', 'claytotal_r', 'dbthirdbar_r', 'wthirdbar_r', 'wfifteenbar_r',
                     'hzdepb_r', 'muname', 'ksat_r', 'resdept_r', 'wsatiated_r']

    # Optional: Verify 'muname' consistency within groups
    inconsistent_groups = df_major_components_oi.groupby(['mukey', 'cokey', 'hzdepb_r'])['muname'].nunique()
    inconsistent_groups = inconsistent_groups[inconsistent_groups > 1]

    if not inconsistent_groups.empty:
        print(
            "Warning: Some groups have multiple 'muname' values. They will be aggregated using the specified function.")
        # Handle accordingly, e.g., use concatenate_unique

    multi_df = df_major_components_oi.pivot_table(
        index=['mukey', 'cokey', 'hzdepb_r'],
        values=values_column,
        aggfunc=agg_funcs
    )

    map_llwc = create_map_ll_water_content(df=df_major_components_oi, multi_df_param_=multi_df)
    map_wsatiated = create_map_wsatiated(df=df_major_components_oi, multi_df_param_=multi_df)
    map_titles = create_map_titles(df=df_major_components_oi, multi_df_param_=multi_df)

    # Step #: name the GEN files:
    # Use similar naming as the SIN and MIS files. - Each major component is going to have a unique SIN, MIS, and GEN file.

    df_major_components_oi.apply(lambda row: update_gen(gen_fpath, row, multi_df, map_llwc, map_wsatiated, map_titles, gen_file_template), axis=1)
