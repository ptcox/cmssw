#include "SimGeneral/MixingModule/interface/DigiAccumulatorMixModFactory.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "SimMuon/CSCDigitizer/src/CSCDigiProducer.h"
#include "SimMuon/CSCDigitizer/src/CSCDigiDump.h"
#include "SimMuon/CSCDigitizer/src/CSCNeutronWriter.h"

DEFINE_DIGI_ACCUMULATOR(CSCDigiProducer);
DEFINE_FWK_MODULE(CSCDigiDump);
DEFINE_FWK_MODULE(CSCNeutronWriter);
