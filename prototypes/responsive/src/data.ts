import type { MediaItem, MediaPresentation, MediaSource, Profile, PlaybackSession } from '../vendor/wire';
import init, { normalize } from '../vendor/viptv_core.js';

// Fictional editorial fixtures. Normalization and presentation decisions run in the pinned Rust WASM.
export async function loadFixtures() {
  await init();
  const project = <T,>(kind: string, data: unknown): T => JSON.parse(normalize(kind, JSON.stringify(data), 'https://example.test'));
  const titles = ['The quiet earth', 'A place between', 'North of nowhere', 'After the tide', 'Another morning', 'Last light'];
  const descriptions = [
    'At the edge of a changing world, a small research team returns to a place everyone else has left behind.',
    'Two strangers find an unexpected connection on the last train through the mountains.',
    'A journey into the far north becomes a story about the people we choose to call home.',
    'When the water recedes, a coastal town begins to uncover its own history.',
    'An ordinary day takes an extraordinary turn in this intimate portrait of a city waking up.',
    'A photographer follows the fading summer light across a landscape of unanswered questions.',
  ];
  const items = titles.map((name, index) => project<MediaItem>('media', {
    id: `demo-${index}`, type: index === 0 ? 'series' : 'movie', name,
    ...(index===0 || index===3 ? {logo:`/art/title-${index}.svg`} : {}),
    background: `/art/landscape-${index}.svg`, poster: `/art/poster-${index}.svg`,
    description: descriptions[index], year: 2026 - index, genres: index % 2 ? ['Drama'] : ['Adventure', 'Drama'],
    position: index === 0 ? 1240 : index === 2 ? 580 : 0, duration: index === 0 ? 2940 : 6300,
    ...(index === 0 ? {season: 1, episode: 3, episode_title: 'Signals from the valley', series_id: 'demo-series'} : {}),
    episodes: index === 0 ? [1,2,3,4].map(episode => ({id:`demo-episode-${episode}`,type:'episode',name:['Arrival','The weather station','Signals from the valley','A different sky'][episode-1],season:1,episode,series_id:'demo-series',thumbnail:`/art/landscape-${episode}.svg`,duration:2940,position:episode===3?1240:0,description:['The team returns to the valley, where a familiar signal leads them into unfamiliar territory.','An empty weather station offers the first clue to what happened before the evacuation.','A message from beyond the ridge challenges everything the team believes about their mission.','As the storm breaks, the team must choose between the route home and one last unanswered question.'][episode-1]})) : [],
  }));
  const sources = [
    {id:'demo-direct',name:'Original · 1080p',title:'Original quality · English audio',provider:'Fixture library',quality:'1080p'},
    {id:'demo-alternate',name:'Alternate · 720p',title:'English audio · alternate source',provider:'Fixture library',quality:'720p'},
  ].map(source => project<MediaSource>('source', source));
  const profiles: Profile[] = [{id:'profile-main',name:'Alex',primary:true,setupComplete:true,raw:{}},{id:'profile-kids',name:'Kids',kid:true,setupComplete:true,raw:{}}];
  const playback: PlaybackSession = {id:'demo-session',url:'https://example.test/media/demo',headers:{},format:'mp4',mode:'direct',videoMode:'copy',audioMode:'copy',position:1240,duration:2940,live:false,audioTracks:[{inputIndex:0,language:'en',languageStatus:'confirmed',title:'English',selected:true,supported:true,selectable:true}],subtitleTracks:[{inputIndex:1,language:'en',languageStatus:'confirmed',title:'English CC',selected:false,supported:true,selectable:true}],subtitlesSupported:true};
  return { items, sources, profiles, playback, present:(item:MediaItem) => project<MediaPresentation>('presentation', item) };
}
export type Fixtures = Awaited<ReturnType<typeof loadFixtures>>;
