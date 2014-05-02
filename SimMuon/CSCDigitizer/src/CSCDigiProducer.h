#ifndef CSCDigiProducer_h
#define CSCDigiProducer_h

#include "SimGeneral/MixingModule/interface/DigiAccumulatorMixMod.h"
#include "FWCore/Framework/interface/ConsumesCollector.h"
#include "SimMuon/CSCDigitizer/src/CSCDigitizer.h"
#include "SimDataFormats/TrackingHit/interface/PSimHitContainer.h"

#include <string>

class CSCStripConditions;
namespace edm {
  namespace one {
    class EDProducerBase;
  }
  class Event;
  class EventSetup;
  class ParameterSet;
  template<typename T> class Handle;
}

class CSCDigiProducer : public DigiAccumulatorMixMod {
public:
  typedef CSCDigitizer::DigiSimLinks DigiSimLinks;

  CSCDigiProducer(const edm::ParameterSet& ps, edm::one::EDProducerBase& mixMod, edm::ConsumesCollector& iC );
  virtual ~CSCDigiProducer();

  virtual void initializeEvent(edm::Event const& e, edm::EventSetup const& c) override;
  virtual void accumulate(edm::Event const& e, edm::EventSetup const& c) override;
  virtual void accumulate(PileUpEventPrincipal const& e, edm::EventSetup const& c) override;
  virtual void finalizeEvent(edm::Event& e, edm::EventSetup const& c) override;

private:
  void accumulateSimHits(edm::Handle<edm::PSimHitContainer>);

  CSCDigitizer theDigitizer_;
  CSCStripConditions * theStripConditions_;
  std::string geomType_;;
  edm::InputTag inputTag_;
  edm::EDGetTokenT<edm::PSimHitContainer> ctoken_; 
  std::map<int, edm::PSimHitContainer> hitMap_;
};

#endif

