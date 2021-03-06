/**
 * Tools for handling citations from the American Chemical Society
 *
 * @module acs
 * @author jmcarp
 */

new PublisherDetector.MetaPublisherDetector('acs', [
    ['name', 'dc.Publisher'],
    ['content', 'American Chemical Society'],
]);

new CitationExtractor.MetaCitationExtractor('acs');

new ReferenceExtractor.SelectorReferenceExtractor(
    'acs',
    'div.NLM_citation'
);