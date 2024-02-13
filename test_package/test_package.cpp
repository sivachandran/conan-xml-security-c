#include <xercesc/util/PlatformUtils.hpp>
#include <xsec/utils/XSECPlatformUtils.hpp>

int main() {
    xercesc::XMLPlatformUtils::Initialize();
    XSECPlatformUtils::Initialise();
    return 0;
}
