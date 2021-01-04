
pad_list = open('pads_list.txt', 'r').read().splitlines()
sup_list = open('supply_list.txt', 'r').read().splitlines()
dut_pat_f = open('arbel_dut_pat.inc', 'w')
dut_iso_f = open('arbel_iso.v', 'w')
pat_setup_f = open('patterns_setup.e', 'w')

# Write arbel_dut_pat.inc
# -----------------------

# dut instance
dut_pat_f.write('arbel_top_taa0 dut(\n')
for pad in pad_list:
    dut_pat_f.write('    .{}({}__dut),\n'.format(pad, pad))

# Add supplies
for line in sup_list:
    dut_pat_f.write(line + '\n')

# iso instance
dut_pat_f.write('\n\n\narbel_iso arbel_iso(\n')
for pad in pad_list:
    dut_pat_f.write('    .{}({}__dut),\n'.format(pad, pad))
    dut_pat_f.write('    .{}({})'.format(pad, pad))
    if pad != pad_list[-1]:
        dut_pat_f.write(',\n')
dut_pat_f.write('\n}; // End of arbel_iso\n\n\n\n')


# Write arbel_iso.v
# -----------------------
dut_iso_f.write('module arbel_iso(\n')
for pad in pad_list:
    dut_iso_f.write('    {}__dut,\n'.format(pad))
    dut_iso_f.write('    {}'.format(pad))
    if pad != pad_list[-1]:
        dut_iso_f.write(',\n')
dut_iso_f.write('\n); // End of arbel_iso\n\n\n')

for pad in pad_list:
    dut_iso_f.write('    //---- {}\n'.format(pad))
    dut_iso_f.write('    inout {}__dut;\n'.format(pad))
    dut_iso_f.write('    inout {};\n'.format(pad))
    dut_iso_f.write('    reg {}__connect;\n'.format(pad))
    dut_iso_f.write('    initial {}__connect = 1\'b0;\n'.format(pad))
    dut_iso_f.write('    tranif1({}, {}__dut, {}__connect);\n\n'.format(pad, pad, pad))

dut_iso_f.write('\nendmodule\n')

# Write patterns setup
# -------------------
pat_setup_f.write('<\'\nextend wb_yarkon_smp_u {\n')
for pad in pad_list:
    pat_setup_f.write('    def_hwp {}__connect of bit = "arbel_iso/{}__connect";\n'.format(pad, pad))
pat_setup_f.write('}  -- End of  wb_yarkon_smp_u\n\n\'>')
