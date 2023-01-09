import './NetworkButton.css'

export default function NetworkButton(props) {
    return (
        <>
            <div onClick={props.onClick} className={`${props.className}`}>
                <h2 className='network-button-id'>#{props.id}</h2>
                {props.nodes && <p className='network-button-timestamp'> Nós: {props.nodes}</p>}
                {props.edges && <p className='network-button-timestamp'> Arestas: {props.edges}</p>}
                {props.communitiesNumber && <p className='network-button-timestamp'> Número de comunidades: {props.communitiesNumber}</p>}
                {props.modularity && <p className='network-button-timestamp'> Modularidade: {props.modularity}</p>}
                {props.averageDegree && <p className='network-button-timestamp'> Grau médio: {props.averageDegree}</p>}
                {props.averageWeight && <p className='network-button-timestamp'> Peso médio: {props.averageWeight}</p>}
                {props.averageClustering && <p className='network-button-timestamp'> Média de clusterização: {props.averageClustering}</p>}
            </div>
        </>
    );
}