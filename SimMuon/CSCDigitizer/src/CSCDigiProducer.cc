#include "SimMuon/CSCDigitizer/src/CSCDigiProducer.h"

#include "DataFormats/Common/interface/Handle.h"

#include "Geometry/CSCGeometry/interface/CSCGeometry.h"
#include "Geometry/Records/interface/MuonGeometryRecord.h"

#include "MagneticField/Records/interface/IdealMagneticFieldRecord.h"

#include "SimMuon/CSCDigitizer/src/CSCConfigurableStripConditions.h"
#include "SimMuon/CSCDigitizer/src/CSCDbStripConditions.h"

#include "SimGeneral/HepPDTRecord/interface/ParticleDataTable.h"
#include "SimGeneral/MixingModule/interface/PileUpEventPrincipal.h"

#include "FWCore/Framework/interface/one/EDProducer.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "FWCore/Utilities/interface/InputTag.h"
#include "FWCore/Utilities/interface/RandomNumberGenerator.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/EventSetup.h"
#include "FWCore/Framework/interface/ESHandle.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/MessageLogger/interface/MessageLogger.h"

CSCDigiProducer::CSCDigiProducer(const edm::ParameterSet& ps, edm::one::EDProducerBase& mixMod, 
   edm::ConsumesCollector& iC ) : theDigitizer_(ps), theStripConditions_(0)
{

  //  LogTrace("CSCDigitizer") << "CSCDigiProducer: in constructor";

  mixMod.produces<CSCWireDigiCollection>("MuonCSCWireDigi");
  mixMod.produces<CSCStripDigiCollection>("MuonCSCStripDigi");
  mixMod.produces<CSCComparatorDigiCollection>("MuonCSCComparatorDigi");
  mixMod.produces<DigiSimLinks>("MuonCSCWireDigiSimLinks");
  mixMod.produces<DigiSimLinks>("MuonCSCStripDigiSimLinks");

  std::string stripConditions( ps.getParameter<std::string>("stripConditions") );
  geomType_ = ps.getParameter<std::string>("GeometryType"); //set member var
  edm::ParameterSet stripPSet = ps.getParameter<edm::ParameterSet>("strips");
  if( stripConditions == "Configurable" )
  {
    theStripConditions_ = new CSCConfigurableStripConditions(stripPSet);
  }
  else if ( stripConditions == "Database" )
  {
    theStripConditions_ = new CSCDbStripConditions(stripPSet);
  }
  else
    {
      throw cms::Exception("CSCDigiProducer") 
	<< "Bad option for strip conditions: "
	<< stripConditions;
    }
  theDigitizer_.setStripConditions(theStripConditions_);

  edm::Service<edm::RandomNumberGenerator> rng;
  if ( ! rng.isAvailable()) {
    throw cms::Exception("Configuration")
      << "CSCDigitizer requires the RandomNumberGeneratorService\n"
      "which is not present in the configuration file.  You must add the service\n"
      "in the configuration file or remove the modules that require it.";
  }

  CLHEP::HepRandomEngine& engine = rng->getEngine();

  theDigitizer_.setRandomEngine(engine);
  theStripConditions_->setRandomEngine(engine);

  std::string inputHits = ps.getParameter<std::string>("InputHits");
  std::string inputHitsInstance = ps.getParameter<std::string>("InputHitsInstance");
  inputTag_ =  edm::InputTag(inputHits, inputHitsInstance); // set member var
  ctoken_ = iC.consumes<edm::PSimHitContainer>( inputTag_ ); // set member var

  LogTrace("CSCDigitizer") << "CSCDigiProducer set " << inputTag_;
}

CSCDigiProducer::~CSCDigiProducer()
{
  delete theStripConditions_;
}

void CSCDigiProducer::initializeEvent(edm::Event const& event, edm::EventSetup const& eventSetup) {
  LogTrace("CSCDigitizer") << "CSCDigiProducer::initializeEvent " << event.id().event() << " - IN - size of hitMap_ = " << hitMap_.size();
  // Clear buffer of simhits from previous event (if any)
  hitMap_.clear();
  LogTrace("CSCDigitizer") << "CSCDigiProducer::initializeEvent " << event.id().event() << " - OUT - size of hitMap_ = " << hitMap_.size();
}

void CSCDigiProducer::accumulate(edm::Event const& event, edm::EventSetup const& eventSetup) {
  LogTrace("CSCDigitizer") << "CSCDigiProducer::accumulate for event " << event.id().event();
  edm::Handle<edm::PSimHitContainer> hsimhits;
  //  event.getByToken(ctoken_, hsimhits);
  event.getByLabel(inputTag_, hsimhits);
  accumulateSimHits(hsimhits);
}

void CSCDigiProducer::accumulate(PileUpEventPrincipal const& event, edm::EventSetup const& eventSetup) {
  //  LogTrace("CSCDigitizer") << "CSCDigiProducer: accumulate PileUpEventPrincipal";
  edm::Handle<edm::PSimHitContainer> hsimhits;
  //  event.getByToken(ctoken_, hsimhits);
  // No getByToken function yet?!
  event.getByLabel(inputTag_, hsimhits);
  accumulateSimHits(hsimhits);
}

void CSCDigiProducer::accumulateSimHits(edm::Handle<edm::PSimHitContainer> hsimhits){
  if(hsimhits.isValid()) {
    // std::map<int, edm::PSimHitContainer> hitMap;  // MAKE THIS A DATA MEMBER
    edm::PSimHitContainer const& hits = *hsimhits.product();
    for ( std::vector<PSimHit>::const_iterator it=hits.begin(); it!=hits.end(); ++it ) {
      unsigned int detId = (*it).detUnitId();
      hitMap_[detId].push_back(*it);
    }
  }
}

void CSCDigiProducer::finalizeEvent(edm::Event& event, const edm::EventSetup& eventSetup) {
  // USED TO BE produce: simhits from event using getByLabel, and filled hitMap in CSCDigitizer::doAction
  // Now hitMap already filled in accumulateSimHits

  // Create empty output
  std::auto_ptr<CSCWireDigiCollection> pWireDigis(new CSCWireDigiCollection());
  std::auto_ptr<CSCStripDigiCollection> pStripDigis(new CSCStripDigiCollection());
  std::auto_ptr<CSCComparatorDigiCollection> pComparatorDigis(new CSCComparatorDigiCollection());
  std::auto_ptr<DigiSimLinks> pWireDigiSimLinks(new DigiSimLinks() );
  std::auto_ptr<DigiSimLinks> pStripDigiSimLinks(new DigiSimLinks() );

  LogTrace("CSCDigitizer") << "CSCDigiProducer::finalizeEvent for event " << event.id().event() << " with " << hitMap_.size() << " simhits";

  //@@ DOES NOTHING IF NO HITS
  if(hitMap_.size() > 0) 
  {
    // find the conditions & geometry for this event

    theStripConditions_->initializeEvent(eventSetup);

    edm::ESHandle<CSCGeometry> hGeom;
    eventSetup.get<MuonGeometryRecord>().get(geomType_,hGeom);
    const CSCGeometry *pGeom = &*hGeom;
    theDigitizer_.setGeometry( pGeom );

    // find the magnetic field
    edm::ESHandle<MagneticField> magfield;
    eventSetup.get<IdealMagneticFieldRecord>().get(magfield);
    theDigitizer_.setMagneticField(&*magfield);

    // set the particle table
    edm::ESHandle < ParticleDataTable > pdt;
    eventSetup.getData( pdt );
    theDigitizer_.setParticleDataTable(&*pdt);

    // run the digitizer - HOW BEST TO PASS THE HITMAP?
    theDigitizer_.digitize(hitMap_, *pWireDigis, *pStripDigis, *pComparatorDigis,
                          *pWireDigiSimLinks, *pStripDigiSimLinks);
  }

  // store the digis in the event
  event.put(pWireDigis, "MuonCSCWireDigi");
  event.put(pStripDigis, "MuonCSCStripDigi");
  event.put(pComparatorDigis, "MuonCSCComparatorDigi");
  event.put(pWireDigiSimLinks, "MuonCSCWireDigiSimLinks");
  event.put(pStripDigiSimLinks, "MuonCSCStripDigiSimLinks");

}

