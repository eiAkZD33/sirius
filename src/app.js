const { algoliasearch, instantsearch } = window;

const searchClient = algoliasearch('QABRKOC7TM', 'd7f64323e5752ad4e20d8536fb9cc1b7');

const search = instantsearch({
  indexName: 'pdf',
  searchClient,
  
});

search.addWidgets([
  instantsearch.widgets.searchBox({
    container: '#searchbox',
  }),
  instantsearch.widgets.hits({
    container: '#hits',
    templates: {
      item: `
      <div>
        <a href="https://ipfs.io/ipfs/{{ipfs_hash}}">{{file_name}}</a>
      </div>
      `,
    },
  }),
  instantsearch.widgets.configure({
    hitsPerPage: 8,
  }),
  instantsearch.widgets.dynamicWidgets({
    container: '#dynamic-widgets',
    fallbackWidget({ container, attribute }) {
      return instantsearch.widgets.panel({ templates: { header: () => attribute } })(
        instantsearch.widgets.refinementList
      )({
        container,
        attribute,
      });
    },
    widgets: [
    ],
  }),
  instantsearch.widgets.pagination({
    container: '#pagination',
  }),
]);

search.start();
