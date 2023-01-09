import { useState } from 'react';
import { useCallback, useRef } from 'react';
import { toPng } from 'html-to-image';
import { FiDownload } from 'react-icons/fi'

import ForceGraph2D from 'react-force-graph-2d';
import NetworkButton from '../../components/NetworkButton/NetworkButton';
import Loader from '../../components/loader/Loader';
import Slider from '@mui/material/Slider';

import './ForceGraph.css'

import DataJson from '../../assets/finalMonth01score05.json'


export default function ForceGraphPageMonth() {

    const [id, setId] = useState(0);

    const [loader, setLoader] = useState(false);

    const ref = useRef(null);

    const graphs = { ...DataJson };

    const marks = graphs.graphTimeline.map((item,index)=>{
       return(
        {
            value: index,
            label: (index+1).toString()
        }
       )
    })

    const displayLoader = () => {
        setLoader(true);
        // setTimeout(() => {
        //     setLoader(false);
        // }, 100);
    }

    const downloadImage = useCallback(() => {
        if (ref.current === null) {
            return
        }

        toPng(ref.current, { cacheBust: true, })
            .then((dataUrl) => {
                const link = document.createElement('a')
                link.download = 'network-snapshot.png'
                link.href = dataUrl
                link.click()
            })
            .catch((err) => {
                console.log(err)
            })
    }, [ref])

    return (
        <>
            <div className='main-page'>

                <div>
                    <Slider
                        style={{ width: '100%' }}
                        max={3}
                        defaultValue={0}
                        value={id}
                        onChange={e => { setId(e.target.value); displayLoader(); }}
                        step={1}
                        marks={marks}
                    />

                </div>

                <div className='page-container'>
                    <div className='page-buttons-container'>
                        {
                            graphs.graphTimeline.map((graph, index) =>
                                <NetworkButton
                                    id={index + 1}
                                    key={index}
                                    nodes={graph.nodesNumber}
                                    edges={graph.edgesNumber}
                                    communitiesNumber={graph.communitiesNumber}
                                    modularity={graph.modularity}
                                    averageDegree={graph.averageDegree}
                                    averageWeight={graph.averageWeight}
                                    averageClustering={graph.averageClustering}
                                    onClick={() => { setId(index); displayLoader(); }}
                                    className={id == index ? 'network-button-selected' : 'network-button-container'}
                                />
                            )
                        }

                    </div>

                    <div className='page-graph-container'>
                        <span className='page-graph-id-label'>
                            <h2 className='page-graph-id-label-text'>#{id + 1}</h2>
                        </span>

                        <button className='page-graph-download-network-button' onClick={downloadImage}><FiDownload /></button>

                        {graphs.graphTimeline.map((graph, index) =>
                            id == index ?
                                <div ref={ref} className='canva-container'>

                                    {
                                        loader == true &&
                                        <div className="loader-container">
                                            <Loader />
                                        </div>
                                    }
                                    <ForceGraph2D
                                        key={index}
                                        linkDirectionalArrowLength={6}
                                        linkDirectionalArrowRelPos={3}                            
                                        linkLabel={"weight"}
                                        graphData={graph}
                                        nodeId="id"
                                        nodeLabel="id"
                                        nodeDesc="id"
                                        nodeColor={node => node.color}
                                        backgroundColor={'white'}
                                        warmupTicks={10}
                                        cooldownTicks={0}
                                        d3VelocityDecay={0.5}
                                        d3AlphaDecay={0.1}
                                        onEngineStop={()=>{setLoader(false);}}

                                    />

                                </div>
                                : <></>
                        )}
                    </div>
                </div>
            </div>

        </>
    );
}
