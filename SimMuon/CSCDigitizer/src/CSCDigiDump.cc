#include "SimMuon/CSCDigitizer/src/CSCDigiDump.h"
#include "DataFormats/Common/interface/Handle.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/MessageLogger/interface/MessageLogger.h"
#include "FWCore/Utilities/interface/InputTag.h"
#include <iostream>

CSCDigiDump::CSCDigiDump(edm::ParameterSet const& conf)
{  
  wd_token = consumes<CSCWireDigiCollection>(conf.getParameter<edm::InputTag>("wireDigiTag"));
  sd_token = consumes<CSCStripDigiCollection>(conf.getParameter<edm::InputTag>("stripDigiTag"));
  cd_token = consumes<CSCComparatorDigiCollection>(conf.getParameter<edm::InputTag>("comparatorDigiTag"));
}


void CSCDigiDump::analyze(edm::Event const& e, edm::EventSetup const& c) {
  edm::Handle<CSCStripDigiCollection> strips;
  edm::Handle<CSCWireDigiCollection> wires;
  edm::Handle<CSCComparatorDigiCollection> comparators;

  std::cout << "Event " << e.id() << std::endl;

  e.getByToken(wd_token, wires);

  int nwd = 0;
  for (CSCWireDigiCollection::DigiRangeIterator j=wires->begin(); j!=wires->end(); j++) {
    std::cout << "Wire digis from "<< CSCDetId((*j).first) << std::endl;
    std::vector<CSCWireDigi>::const_iterator digiItr = (*j).second.first;
    std::vector<CSCWireDigi>::const_iterator last = (*j).second.second;
    for( ; digiItr != last; ++digiItr) {
      ++nwd;
      digiItr->print();
    }
  }
  std::cout << "Event " << e.id() << ": no. of wire digis = "  << nwd << std::endl;

  e.getByToken(sd_token, strips);

  int nsd = 0;
  for (CSCStripDigiCollection::DigiRangeIterator j=strips->begin(); j!=strips->end(); j++) {
    std::cout << "Strip digis from "<< CSCDetId((*j).first) << std::endl;
    std::vector<CSCStripDigi>::const_iterator digiItr = (*j).second.first;
    std::vector<CSCStripDigi>::const_iterator last = (*j).second.second;
    for( ; digiItr != last; ++digiItr) {
      ++ nsd;
      digiItr->print();
    }
  }
  std::cout << "Event " << e.id() << ": no. of strip digis = "  << nsd << std::endl;

  e.getByToken(cd_token, comparators);

  int ncd = 0;
  for (CSCComparatorDigiCollection::DigiRangeIterator j=comparators->begin(); 
       j!=comparators->end(); j++) 
  {
    std::cout << "Comparator digis from "<< CSCDetId((*j).first) << std::endl;
    std::vector<CSCComparatorDigi>::const_iterator digiItr = (*j).second.first;
    std::vector<CSCComparatorDigi>::const_iterator last = (*j).second.second;
    for( ; digiItr != last; ++digiItr) {
      ++ncd;
      digiItr->print();
    }
  }
  std::cout << "Event " << e.id() << ": no. of comparator digis = "  << nwd << std::endl;
}


