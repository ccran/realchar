import Tabs from './_components/Tabs';

import { getCharacters } from '../util/apiSsr';

export default async function Page() {
  const characters = await getCharacters();
  console.log("characters:" + JSON.stringify(characters))

  return (
    <>
      {/* <Header /> */}
      <div className='py-6 md:py-10 px-4 md:px-6 lg:px-14 container mx-auto'>
        <h1 className='text-center font-light text-3xl'>
          Real-time communication with your AI character
        </h1>
        <Tabs characters={characters} />
      </div>
      {/* <Footer /> */}
    </>
  );
}
