<%inherit file="../resource_rdf.mako"/>
<%block name="properties">
    <rdf:type rdf:resource="${str(h.rdf.NAMESPACES['skos']['Concept'])}"/>
    % for vs in ctx.valuesets:
    <dcterms:hasPart rdf:resource="${request.resource_url(vs)}"/>
    % endfor
    % for de in ctx.domain:
    <skos:narrower rdf:resource="${de.url(request)}"/>
    % endfor
</%block>
<%block name="resources">
    % for de in ctx.domain:
    <dcterms:Standard rdf:about="${de.url(request)}">
        <rdf:type rdf:resource="${str(h.rdf.NAMESPACES['skos']['Concept'])}"/>
        <rdfs:label xml:lang="en">${de}</rdfs:label>
        <skos:prefLabel xml:lang="en">${de}</skos:prefLabel>
        <dcterms:title xml:lang="en">${de}</dcterms:title>
        % if getattr(de, 'description'):
        <dcterms:description xml:lang="en">${de.description}</dcterms:description>
        % endif
        <skos:broader rdf:resource="${request.resource_url(ctx)}"/>
        % if de.number is not None:
        <dcterms:description rdf:datatype="http://www.w3.org/2001/XMLSchema#int">${de.number}</dcterms:description>
        % endif
    </dcterms:Standard>
    % endfor
</%block>
