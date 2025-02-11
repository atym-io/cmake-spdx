# SPDX-License-Identifier: Apache-2.0

import argparse
import glob
import os

import sbom

excludeDirs = [".git/"]

def makeSpdxFromCmakeReply(buildDir: str, outputDir: str, ns: str, documentNamePrefix: str):
    indexSearchPath = os.path.join(buildDir, '.cmake/api/v1/reply', 'index-*.json')
    indexFiles = glob.glob(indexSearchPath)

    if len(indexFiles) == 0:
        print(f"Couldn't find index JSON file in {indexSearchPath}")
        exit(1)

    config = sbom.Config(
        replyIndexPath=indexFiles[0],
        spdxOutputDir=outputDir,
        spdxNamespacePrefix=ns,
        excludeDirs=excludeDirs,
        documentNamePrefix=documentNamePrefix,
    )

    sbom.makeSpdxFromCmakeReply(config)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog='cmake-spdx',
        description="Generate SPDX from CMake File API index",
    )

    parser.add_argument('-b', '--build-dir', help='Path to CMake build directory', required=True)
    parser.add_argument('-o', '--output-dir', help='Output directory for SPDX files', required=True)
    parser.add_argument('-n', '--ns', help='Namespace prefix for SPDX files', required=True)
    parser.add_argument('--doc-name-prefix', help='Document name prefix', default='')

    args = parser.parse_args()

    makeSpdxFromCmakeReply(
        buildDir=args.build_dir,
        outputDir=args.output_dir,
        ns=args.ns,
        documentNamePrefix=args.doc_name_prefix,
    )
