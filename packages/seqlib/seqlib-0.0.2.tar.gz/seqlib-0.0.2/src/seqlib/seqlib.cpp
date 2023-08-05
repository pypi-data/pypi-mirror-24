#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

#include "htslib/htslib/sam.h"

#include "SeqLib/BWAWrapper.h"
#include "SeqLib/RefGenome.h"

// #include "seqlib_to_pysam/seqlib_to_pysam_api.h"

namespace py = pybind11;
using namespace SeqLib;


// std::vector<py::handle> 
BamRecordVector align(SeqLib::BWAWrapper const &bwa, const std::string& seq, const std::string& read_name,
                              bool hardclip, double secondary_hit_cutoff, int max_secondary) {
    BamRecordVector alignments;
    std::vector<py::handle> alignedSegments;

    // import_seqlib_to_pysam();

    bwa.AlignSequence(seq, read_name, alignments, hardclip, secondary_hit_cutoff, max_secondary);

    return alignments;
    // for (auto& aln : alignments) {
    //     alignedSegments.push_back(py::handle(convertBam1tToAlignedSegment(aln.raw())));
    // }

    // return alignedSegments;
}


PYBIND11_PLUGIN(_seqlib) {
    py::module seq_lib_module("seqlib", "seqlib interface");

    py::class_<SeqLib::BWAWrapper, std::shared_ptr<SeqLib::BWAWrapper>>(seq_lib_module, "BWAWrapper", "Run BWA in-memory")
        .def(py::init<>()) // this could take a list of alignment parameters with defaults, eg gap open=x, etc

        .def("loadIndex", &SeqLib::BWAWrapper::LoadIndex, "Load a BWA index", py::arg("index"))
        .def("makeIndex", [](SeqLib::BWAWrapper &bwa, std::unordered_map<std::string, std::string>namesToSeqs, std::vector<std::string>orderedNames ) {
            UnalignedSequenceVector usv;
            //for (auto& kv : namesToSeqs) {
	    for (auto& key : orderedNames) {
	      usv.push_back(UnalignedSequence(key, namesToSeqs[key]));
		//usv.push_back(UnalignedSequence(kv.first, kv.second));
            }
            bwa.ConstructIndex(usv);
        })
        
        .def("align", &align, "Align the provided sequence against the loaded BWA index",
             py::arg("seq"), py::arg("read_name") = "read", py::arg("hardclip") = true,
             py::arg("secondary_hit_cutoff") = 0.9, py::arg("max_secondary") = 10)
        
        .def("ChrIDToName", &SeqLib::BWAWrapper::ChrIDToName, "Retrieve the sequence name from its numeric ID")



        .def("SetMinSeedLength", &SeqLib::BWAWrapper::SetMinSeedLength)
        .def("SetMinChainWeight", &SeqLib::BWAWrapper::SetMinChainWeight)

        .def("SetGapOpen", &SeqLib::BWAWrapper::SetGapOpen)
        .def("SetGapExtension", &SeqLib::BWAWrapper::SetGapExtension)
        .def("SetMismatchPenalty", &SeqLib::BWAWrapper::SetMismatchPenalty)
        .def("SetReseedTrigger", &SeqLib::BWAWrapper::SetReseedTrigger)
        .def("SetBandwidth", &SeqLib::BWAWrapper::SetBandwidth)
        .def("SetZDropoff", &SeqLib::BWAWrapper::SetZDropoff)
        .def("Set3primeClippingPenalty", &SeqLib::BWAWrapper::Set3primeClippingPenalty)
        .def("Set5primeClippingPenalty", &SeqLib::BWAWrapper::Set5primeClippingPenalty)
        .def("SetAScore", &SeqLib::BWAWrapper::SetAScore)


        .def("__len__", [](SeqLib::BWAWrapper const &o) -> int { return o.NumSequences(); } )
        .def("__str__", [](SeqLib::BWAWrapper const &o) -> std::string { std::ostringstream s; s << o; return s.str(); } );


    py::class_<SeqLib::BamRecord>(seq_lib_module, "BamRecord", "Represents a bam alignment")
        .def("ReverseFlag", &SeqLib::BamRecord::ReverseFlag)
        .def("QualitySequence", &SeqLib::BamRecord::QualitySequence)
        .def("Position", &SeqLib::BamRecord::Position)
        .def("ChrID", &SeqLib::BamRecord::ChrID)
        .def("AlignmentFlag", &SeqLib::BamRecord::AlignmentFlag)

        .def("Qname", &SeqLib::BamRecord::Qname)
        .def("CigarString", &SeqLib::BamRecord::CigarString)
        .def("Sequence", &SeqLib::BamRecord::Sequence)

        // ** note that we can't access the tags yet! see pysam.AlignedSegment.get_tags() **
        // .def("tags", &SeqLib::BamRecord::) 

        // .def("", &SeqLib::BamRecord::)

        .def("__str__", [](SeqLib::BamRecord const &o) -> std::string { std::ostringstream s; s << o; return s.str(); } );

        ;

    return seq_lib_module.ptr();
}
