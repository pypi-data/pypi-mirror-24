#!/bin/env python
# | Copyright 2013-2017 Karlsruhe Institute of Technology
# |
# | Licensed under the Apache License, Version 2.0 (the "License");
# | you may not use this file except in compliance with the License.
# | You may obtain a copy of the License at
# |
# |     http://www.apache.org/licenses/LICENSE-2.0
# |
# | Unless required by applicable law or agreed to in writing, software
# | distributed under the License is distributed on an "AS IS" BASIS,
# | WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# | See the License for the specific language governing permissions and
# | limitations under the License.

_GEO_DICT = {
	'cam.ac.uk': (52.204451, 0.110865),
	'lebedev.ru': (55.697663, 37.565417),
	'tamu.edu': (30.606743, -96.349611),
	'shef.ac.uk': (53.379258, -1.492002),
	'metu.edu.tr': (39.890904, 32.784734),
	'ucl.ac.be': (50.668504, 4.612838),
	'technion.ac.il': (32.777443, 35.021707),
	'baylor.edu': (31.541675, -97.121204),
	'bnl.gov': (40.87056, -72.880139),
	'icm.edu.pl': (52.220228, 20.980339),
	'ucy.ac.cy': (35.158933, 33.377094),
	'iihe.ac.be': (50.813921, 4.266747),
	'ifca.es': (43.472356, -3.80373),
	'jet.efda.org': (51.658075, -1.229839),
	'jinr.ru': (56.745899, 37.189393),
	'cornell.edu': (42.446325, -76.477561),
	'wroc.pl': (51.114084, 17.034931),
	'ucsd.edu': (32.875695, -117.232289),
	'sprace.org.br': (-23.523169, -46.667857),
	'dur.scotgrid.ac.uk': (54.7596, -1.578441),
	'umd.edu': (38.985366, -76.939759),
	'ncp.edu.pk': (33.750035, 73.16411),
	'cbpf.br': (-22.953962099999998, -43.173729100000003),
	'kiae.ru': (55.801216500000002, 37.4770295),
	'msu.ru': (55.706713999999998, 37.516877899999997),
	'nd.edu': (41.692463, -86.235824),
	'cinvestav.mx': (19.510706800000001, -99.129099299999993),
	'unina.it': (40.8683537, 14.273237699999999),
	'weizmann.ac.il': (32.111285700000003, 34.801503599999997),
	'nikhef.nl': (52.356160199999998, 4.9506603),
	'ifh.de': (52.376036900000003, 13.6513928),
	'colorado.edu': (39.754908499999999, -105.0234923),
	'ufl.edu': (29.643454, -82.350612),
	'kfki.hu': (46.87404, 17.905941),
	'ciemat.es': (40.454523, -3.728886),
	'knu.ac.kr': (35.891831, 128.610649),
	'kharkov.ua': (50.087988, 36.249275),
	'purdue.edu': (40.427872, -86.913929),
	'vanderbilt.edu': (36.143836, -86.803694),
	'itwm.fhg.de': (49.43085, 7.752557),
	'nectec.or.th': (14.079305, 100.601006),
	'cscs.ch': (47.377589, 8.547853),
	'ohio-state.edu': (40.012891, -83.029404),
	'nhn.ou.edu': (35.208459, -97.445741),
	'tu-dortmund.de': (51.484603, 7.412914),
	'ihep.su': (54.865346, 37.211666),
	'uniandes.edu.co': (4.602947, -74.066248),
	'ultralight.org': (34.141415, -118.124896),
	'rl.ac.uk': (51.573229, -1.31567),
	'rhul.ac.uk': (51.425571, -0.562928),
	'manchester.ac.uk': (53.477013, -2.239208),
	'brunel.ac.uk': (51.533069, -0.473878),
	'ox.ac.uk': (51.75695, -1.257262),
	'bris.ac.uk': (51.457991, -2.601492),
	'qmul.ac.uk': (51.524312, -0.038649),
	'mit.edu': (42.360066, -71.093273),
	'gla.scotgrid.ac.uk': (55.872277, -4.289138),
	'tau.ac.il': (32.111296, 34.801669),
	'liv.ac.uk': (53.404441, -2.964942),
	'ed.ac.uk': (55.945379, -3.191407),
	'hellasgrid.gr': (37.983716, 23.729725),
	'ic.ac.uk': (51.498912, -0.174465),
	'in2p3.fr': (45.783088, 4.865513),
	'wisc.edu': (43.075158, -89.400959),
	'cern.ch': (46.234167, 6.052778),
	'spbu.ru': (59.941148, 30.298315),
	'ttu.edu': (33.585496, -101.871427),
	'infn.it': (41.900712, 12.512133),
	'slac.stanford.edu': (37.418436, -122.205935),
	'rwth-aachen.de': (50.777341, 6.077743),
	'fnal.gov': (41.831968, -88.251858),
	'brown.edu': (41.827107, -71.40295),
	'unl.edu': (40.818226, -96.700001),
	'desy.de': (53.575639, 9.879441),
	'sinica.edu.tw': (25.043459, 121.614486),
}


def get_geo_match(hostname):
	for site in _GEO_DICT:
		if hostname.endswith(site):
			return (site, _GEO_DICT[site][0], _GEO_DICT[site][1])


class GeoResolver(object):
	def __init__(self):
		from grid_control.utils.webservice import JSONRestClient
		self._jrc = JSONRestClient(url='http://maps.googleapis.com/maps/api/geocode/json')

	def run(self):
		# output of lcg-infosites ce | while read X X X X X CE; do echo $CE; done
		#   | cut -d "/" -f 1 | cut -d ":" -f 1 | sort | uniq
		ce_list_str = """alcyone-cms.grid.helsinki.fi
			alice23.spbu.ru
			arc-ce01.gridpp.rl.ac.uk
			arc-ce02.gridpp.rl.ac.uk
			arc-ce03.gridpp.rl.ac.uk
			argoce01.na.infn.it
			atlasce1.lnf.infn.it
			atlasce2.lnf.infn.it
			atlasce3.lnf.infn.it
			atlas-cream01.na.infn.it
			atlas-cream02.na.infn.it
			boce.bo.infn.it
			bonner-grid.rice.edu
			brux3.hep.brown.edu
			cale.uniandes.edu.co
			carter-osg.rcac.purdue.edu
			cccreamceli07.in2p3.fr
			cccreamceli08.in2p3.fr
			cce.ihep.ac.cn
			ce0002.m45.ihep.su
			ce0004.m45.ihep.su
			ce01.cmsaf.mit.edu
			ce01.jinr-t1.ru
			ce01-lcg.cr.cnaf.infn.it
			ce-01.roma3.infn.it
			ce01.tier2.hep.manchester.ac.uk
			ce02.cmsaf.mit.edu
			ce02.jinr-t1.ru
			ce02.ngcc.acad.bg
			ce02.tier2.hep.manchester.ac.uk
			ce04-lcg.cr.cnaf.infn.it
			ce05.esc.qmul.ac.uk
			ce05-lcg.cr.cnaf.infn.it
			ce05.ncg.ingrid.pt
			ce06.esc.qmul.ac.uk
			ce06-lcg.cr.cnaf.infn.it
			ce07.esc.qmul.ac.uk
			ce07-lcg.cr.cnaf.infn.it
			ce08-lcg.cr.cnaf.infn.it
			ce101.grid.ucy.ac.cy
			ce1.accre.vanderbilt.edu
			ce1.dur.scotgrid.ac.uk
			ce1.grid.lebedev.ru
			ce1.ts.infn.it
			ce201.cern.ch
			ce202.cern.ch
			ce203.cern.ch
			ce204.cern.ch
			ce205.cern.ch
			ce206.cern.ch
			ce207.cern.ch
			ce208.cern.ch
			ce2.accre.vanderbilt.edu
			ce2.particles.ipm.ac.ir
			ce301.cern.ch
			ce302.cern.ch
			ce3.ppgrid1.rhul.ac.uk
			ce401.cern.ch
			ce402.cern.ch
			ce403.cern.ch
			ce404.cern.ch
			ce405.cern.ch
			ce406.cern.ch
			ce407.cern.ch
			ce408.cern.ch
			ce64.ipb.ac.rs
			ce6.grid.icm.edu.pl
			ce7.glite.ecdf.ed.ac.uk
			ce9.grid.icm.edu.pl
			cebo-t3-01.cr.cnaf.infn.it
			cebo-t3-02.cr.cnaf.infn.it
			ce.cis.gov.pl
			cecream.ca.infn.it
			ce.fesb.egi.cro-ngi.hr
			ce.grid.unesp.br
			ce.irb.egi.cro-ngi.hr
			ceprod05.grid.hep.ph.ic.ac.uk
			ceprod06.grid.hep.ph.ic.ac.uk
			ceprod07.grid.hep.ph.ic.ac.uk
			ceprod08.grid.hep.ph.ic.ac.uk
			cert-37.pd.infn.it
			ce.scope.unina.it
			ce.srce.egi.cro-ngi.hr
			cetest01.grid.hep.ph.ic.ac.uk
			cetest02.grid.hep.ph.ic.ac.uk
			ce.ulakbim.gov.tr
			cit-gatekeeper2.ultralight.org
			cit-gatekeeper.ultralight.org
			cluster118.knu.ac.kr
			cluster50.knu.ac.kr
			cms-0.mps.ohio-state.edu
			cmsce01.na.infn.it
			cmsgrid01.hep.wisc.edu
			cmsgrid02.hep.wisc.edu
			cms-grid0.hep.uprm.edu
			cmsosgce2.fnal.gov
			cmsosgce4.fnal.gov
			cmsosgce.fnal.gov
			cmsrm-cream01.roma1.infn.it
			cmsrm-cream02.roma1.infn.it
			cmsrm-cream03.roma1.infn.it
			cmstest1.rcac.purdue.edu
			cms.tier3.ucdavis.edu
			conte-osg.rcac.purdue.edu
			cox01.grid.metu.edu.tr
			cr1.ipp.acad.bg
			cream01.grid.auth.gr
			cream01.grid.sinica.edu.tw
			cream01.grid.uoi.gr
			cream01.kallisto.hellasgrid.gr
			cream01.lcg.cscs.ch
			cream02.grid.cyf-kr.edu.pl
			cream02.iihe.ac.be
			cream02.lcg.cscs.ch
			cream03.lcg.cscs.ch
			cream04.grid.sinica.edu.tw
			cream04.lcg.cscs.ch
			cream05.grid.sinica.edu.tw
			cream2.ppgrid1.rhul.ac.uk
			cream3.hep.kbfi.ee
			cream4.hep.kbfi.ee
			cream.afroditi.hellasgrid.gr
			cream-ce01.ariagni.hellasgrid.gr
			cream-ce01.indiacms.res.in
			cream-ce01.marie.hellasgrid.gr
			cream-ce02.cat.cbpf.br
			creamce02.ciemat.es
			cream-ce02.marie.hellasgrid.gr
			creamce03.ciemat.es
			creamce1.itep.ru
			cream-ce-2.ba.infn.it
			cream-ce-4.ba.infn.it
			cream-ce.cat.cbpf.br
			cream-ce.grid.atomki.hu
			creamce.hephy.oeaw.ac.at
			creamce.inula.man.poznan.pl
			cream-ce.kipt.kharkov.ua
			cream-ce.pg.infn.it
			creamce.reef.man.poznan.pl
			cream.grid.cyf-kr.edu.pl
			cream.ipb.ac.rs
			dc2-grid-66.brunel.ac.uk
			dc2-grid-68.brunel.ac.uk
			dc2-grid-70.brunel.ac.uk
			dwarf.wcss.wroc.pl
			earth.crc.nd.edu
			epgr02.ph.bham.ac.uk
			erbium.lsr.nectec.or.th
			f-cream01.grid.sinica.edu.tw
			f-cream04.grid.sinica.edu.tw
			fiupg.hep.fiu.edu
			foam.grid.kiae.ru
			fornax-ce2.itwm.fhg.de
			fornax-ce.itwm.fhg.de
			grcreamce01.inr.troitsk.ru
			grid001.ics.forth.gr
			grid002.jet.efda.org
			grid012.ct.infn.it
			grid01.physics.uoi.gr
			grid0.fe.infn.it
			grid106.kfki.hu
			grid107.kfki.hu
			grid109.kfki.hu
			grid129.sinp.msu.ru
			grid36.lal.in2p3.fr
			grid72.phy.ncu.edu.tw
			gridce01.ifca.es
			gridce03.ifca.es
			gridce0.pi.infn.it
			gridce1.pi.infn.it
			grid-ce2.physik.rwth-aachen.de
			gridce2.pi.infn.it
			gridce3.pi.infn.it
			gridce4.pi.infn.it
			gridce.ilc.cnr.it
			grid-ce.physik.rwth-aachen.de
			grid-cr0.desy.de
			grid-cr1.desy.de
			grid-cr2.desy.de
			grid-cr3.desy.de
			grid-cr4.desy.de
			gridgk01.racf.bnl.gov
			gridgk02.racf.bnl.gov
			gridgk03.racf.bnl.gov
			gridgk04.racf.bnl.gov
			gridgk05.racf.bnl.gov
			gridgk06.racf.bnl.gov
			gridgk08.racf.bnl.gov
			gridtest02.racf.bnl.gov
			gridvm03.roma2.infn.it
			grisuce.scope.unina.it
			gt3.pnpi.nw.ru
			hansen-osg.rcac.purdue.edu
			hepcms-0.umd.edu
			hepgrid10.ph.liv.ac.uk
			hepgrid5.ph.liv.ac.uk
			hepgrid6.ph.liv.ac.uk
			hepgrid97.ph.liv.ac.uk
			hephygr.oeaw.ac.at
			heposg01.colorado.edu
			hurr.tamu.edu
			ingrid.cism.ucl.ac.be
			jade-cms.hip.fi
			juk.nikhef.nl
			kalkan1.ulakbim.gov.tr
			khaldun.biruni.upm.my
			klomp.nikhef.nl
			kodiak-ce.baylor.edu
			lcg18.sinp.msu.ru
			lcg52.sinp.msu.ru
			lcgce01.phy.bris.ac.uk
			lcgce03.phy.bris.ac.uk
			lcgce04.phy.bris.ac.uk
			lcgce12.jinr.ru
			lcgce1.shef.ac.uk
			lcgce21.jinr.ru
			lcgce2.shef.ac.uk
			lcg-cream.ifh.de
			llrcream.in2p3.fr
			lpnhe-cream.in2p3.fr
			lyogrid07.in2p3.fr
			magic.cse.buffalo.edu
			mwt2-gk.campuscluster.illinois.edu
			ndcms.crc.nd.edu
			node01-03.usm.renam.md
			node01-04.grid.renam.md
			node05-02.imi.renam.md
			node74.datagrid.cea.fr
			nodeslab-0002.nlab.tb.hiit.fi
			ntugrid2.phys.ntu.edu.tw
			ntugrid5.phys.ntu.edu.tw
			nys1.cac.cornell.edu
			osgce.hepgrid.uerj.br
			osg-ce.sprace.org.br
			osg-gk.mwt2.org
			osg-gw-6.t2.ucsd.edu
			osg-gw-7.t2.ucsd.edu
			osg.hpc.ufl.edu
			osg-nemo-ce.phys.uwm.edu
			osg.rcac.purdue.edu
			osgserv01.slac.stanford.edu
			osgserv02.slac.stanford.edu
			ouhep0.nhn.ou.edu
			pamelace01.na.infn.it
			pcncp04.ncp.edu.pk
			pcncp05.ncp.edu.pk
			pre7230.datagrid.cea.fr
			prod-ce-01.pd.infn.it
			razi.biruni.upm.my
			recasce01.na.infn.it
			red-gw1.unl.edu
			red-gw2.unl.edu
			red.unl.edu
			rossmann-osg.rcac.purdue.edu
			sbgce2.in2p3.fr
			snf-189278.vm.okeanos.grnet.gr
			snf-458754.vm.okeanos.grnet.gr
			spacina-ce.scope.unina.it
			svr009.gla.scotgrid.ac.uk
			svr010.gla.scotgrid.ac.uk
			svr011.gla.scotgrid.ac.uk
			svr014.gla.scotgrid.ac.uk
			t2arc01.physics.ox.ac.uk
			t2-ce-01.lnl.infn.it
			t2-ce-01.to.infn.it
			t2-ce-02.lnl.infn.it
			t2ce02.physics.ox.ac.uk
			t2-ce-03.lnl.infn.it
			t2-ce-04.lnl.infn.it
			t2-ce-04.mi.infn.it
			t2ce04.physics.ox.ac.uk
			t2-ce-05.mi.infn.it
			t2-ce-06.lnl.infn.it
			t2ce06.physics.ox.ac.uk
			t3serv007.mit.edu
			tau-cream.hep.tau.ac.il
			tech-crm.hep.technion.ac.il
			top.ucr.edu
			umiss001.hep.olemiss.edu
			uosaf0008.sscc.uos.ac.kr
			uscms1.fltech-grid3.fit.edu
			v6ce00.grid.hep.ph.ic.ac.uk
			vserv13.hep.phy.cam.ac.uk
			wipp-crm.weizmann.ac.il
		"""
		import sys, time
		from python_compat import set, imap, lfilter, sorted

		counter = 0
		used = set()
		for line in imap(str.strip, ce_list_str.splitlines()):
			time.sleep(0.2)
			match = get_geo_match(line)
			if not match:
				counter += 1
				sys.stderr.write('\t%r: %r\n' % (line, self._geocode(line)))
			else:
				used.add(match)
		sys.stderr.write('%s unmatched entries\n' % counter)
		sys.stderr.write('unused entries:\n%s\n' % repr(lfilter(lambda x: x not in used, _GEO_DICT)))

		sys.stdout.write('_GEO_DICT = {\n')
		geo_dict_key_list = sorted(_GEO_DICT.keys(), key=lambda x: str.join('.', reversed(x.split('.'))))
		for entry in geo_dict_key_list:
			sys.stdout.write('\t%r: (%.6f, %.6f),\n' % (entry, _GEO_DICT[entry][0], _GEO_DICT[entry][1]))
		sys.stdout.write('}\n')

	def _geocode(self, loc):
		result = self._jrc.get(params={'address': str.join('.', loc.split('.')[2:]), 'sensor': 'false'})
		if 'Placemark' in result:  # unfold placemake entries
			place_list = []
			for entry in result['Placemark']:
				place_list.append((entry['address'], tuple(reversed(entry['Point']['coordinates'][:2]))))
			return place_list
		return result

if __name__ == '__main__':
	GeoResolver().run()
